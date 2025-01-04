from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.base import ContentFile

from audio_surveys import settings
from audio_surveys.models import AudioExamples, AudioSet, MultipleChoiceQuestion, ScaleQuestion, Survey, SurveyAnswer
from .forms import FileFieldForm


def upload_file(request):
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.data["name"]
            audio_set = AudioSet.objects.create(
                name=name
            )
            audio_set.save()

            files = form.cleaned_data["file_field"]
            for idx, file in enumerate(files):
                content_file = ContentFile(
                    file.read(), name=file.name)
                audio_example = AudioExamples.objects.create(
                    audio_example=content_file, name=f"{file.name}", audio_set=audio_set
                )
                audio_example.save()

            return HttpResponseRedirect("/admin/audio_surveys/audioset/")
    else:
        form = FileFieldForm()
    return render(request, "audio_surveys/upload.html", {"form": form})


def survey(request, title):
    if request.method == "POST":
        answers = request.POST

        answers_dict = {key: value for key,
                        value in answers.items() if key != "csrfmiddlewaretoken"}

        answers = []
        for key, value in answers_dict.items():
            data = key.split("|")
            audio_example = data[1].replace("/media/audio_examples/", "")
            question_prompt = data[2]
            answers.append({
                "audio_example": audio_example,
                "question_prompt": question_prompt,
                "question_type": "Multiple Choice" if data[0] == "mcq" else "Scale",
                "answer": value
            })

        survey = Survey.objects.filter(title=title).first()
        survey_answer = SurveyAnswer.objects.create(
            survey=survey, answers=answers)
        survey_answer.save()

        return render(request, "audio_surveys/survey.html", {
            "multiple_choice_questions": [],
            "scale_questions": [],
            "audio_examples": []
        })
    else:
        survey = Survey.objects.filter(title=title).first()

        multiple_choice_questions = MultipleChoiceQuestion.objects.filter(
            survey=survey)
        scale_questions = ScaleQuestion.objects.filter(survey=survey)
        audio_examples = AudioExamples.objects.filter(
            audio_set=survey.audio_set)

        audio_samples = [settings.MEDIA_URL + el[0]
                         for el in audio_examples.values_list("audio_example")]

        multiple_choice_questions = [{"prompt": question.prompt, "choices": question.choices.split(
            ";")} for question in multiple_choice_questions]
        scale_questions = [{"prompt": question.prompt, "degrees": question.degrees}
                           for question in scale_questions]

        return render(request, "audio_surveys/survey.html", {
            "multiple_choice_questions": multiple_choice_questions,
            "scale_questions": scale_questions,
            "audio_examples": audio_samples
        })
