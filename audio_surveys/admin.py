import io
from django.contrib import admin
from django.utils.html import format_html
from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirect
from django.http import HttpResponse
import xlsxwriter

from audio_surveys.forms import AudioSetForm
from .models import AudioExamples, AudioSet, Survey, SurveyAnswer
from .models import MultipleChoiceQuestion, ScaleQuestion
import datetime


class MultipleChoiceQuestionInline(admin.TabularInline):
    model = MultipleChoiceQuestion
    extra = 0


class ScaleQuestionInline(admin.TabularInline):
    model = ScaleQuestion
    extra = 0


@admin.action(description="Export selected surveys as XLSX")
def export_xlsx(modeladmin, request, queryset):
    output = io.BytesIO()
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"survey_export_{date_str}.xlsx"

    workbook = xlsxwriter.Workbook(output)

    answsers_per_question = {}
    for survey in queryset:
        answer_sets = SurveyAnswer.objects.filter(survey=survey)

        for answer_set in answer_sets:
            for answer in answer_set.answers:
                audio_example = answer["audio_example"]
                question_prompt = answer["question_prompt"]
                answer_value = answer["answer"]

                if question_prompt not in answsers_per_question:
                    answsers_per_question[question_prompt] = {}

                if audio_example not in answsers_per_question[question_prompt]:
                    answsers_per_question[question_prompt][audio_example] = []

                answsers_per_question[question_prompt][audio_example].append(
                    answer_value)

    print(answsers_per_question)

    for question_prompt, audio_examples in answsers_per_question.items():
        worksheet_name = question_prompt[:31].replace('[', '').replace(']', '').replace(
            ':', '').replace('*', '').replace('?', '').replace('/', '').replace('\\', '')
        worksheet = workbook.add_worksheet(worksheet_name)
        col = 0
        row = 0

        for audio_example, data in audio_examples.items():
            worksheet.write(row, col, audio_example)
            for answer in data:
                col += 1
                worksheet.write(row, col, answer)
            row += 1
            col = 0  # Reset column for the next audio example

    workbook.close()
    output.seek(0)

    # Set up the Http response.
    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


class SurveyAdmin(admin.ModelAdmin):
    inlines = [
        MultipleChoiceQuestionInline,
        ScaleQuestionInline
    ]
    list_display = ("title", "id", "description", "audio_set", "survey_link")
    actions = [export_xlsx]

    def survey_link(self, obj):
        ROOT_URL = "http://127.0.0.1:8000"  # MOVE
        return format_html(f"<a href='{ROOT_URL}/survey/{obj.title}' target='_blank'>Survey Link</a>")

    survey_link.allow_tags = True


class AudioExamplesAdmin(admin.ModelAdmin):
    list_display = ("name", "audio_set")
    list_filter = ["audio_set"]


class AudioSetAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    @button(label="Upload Audio Examples", css_class="btn btn-primary")
    def upload_audio_examples(self, request):
        return HttpResponseRedirect("/upload_file")


admin.site.register(Survey, SurveyAdmin)
admin.site.register(AudioSet, AudioSetAdmin)
admin.site.register(AudioExamples, AudioExamplesAdmin)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(ScaleQuestion)
admin.site.register(SurveyAnswer)
