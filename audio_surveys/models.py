from django.db import models


class AudioSet(models.Model):
    name = models.CharField(max_length=100, blank=False, default="")

    def __str__(self):
        return f"{self.name}"


class AudioExamples(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "audio_examples/{0}".format(filename)

    audio_example = models.FileField(upload_to=user_directory_path, null=True)
    audio_set = models.ForeignKey(
        AudioSet, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.audio_set.name}: {self.name}"


class Question(models.Model):
    prompt = models.CharField(max_length=100, blank=True, default="")
    survey = models.ForeignKey("Survey", on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Question: {self.prompt}"


class MultipleChoiceQuestion(Question):
    choices = models.TextField()


class ScaleQuestion(Question):
    degrees = models.IntegerField()


class Survey(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    audio_set = models.ForeignKey(
        AudioSet, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Survey: {self.title}"


class SurveyAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    answers = models.JSONField()
