from django.contrib import admin

from .models import Survey
from .models import MultipleChoiceQuestion, ScaleQuestion


class MultipleChoiceQuestionInline(admin.TabularInline):
    model = MultipleChoiceQuestion
    extra = 0


class ScaleQuestionInline(admin.TabularInline):
    model = ScaleQuestion
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    inlines = [
        MultipleChoiceQuestionInline,
        ScaleQuestionInline
    ]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(ScaleQuestion)
