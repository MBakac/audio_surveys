from django.db import models


class AudioSet(models.Model):
    audio_examples = models.FileField(
        upload_to="audio_examples", null=True)


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
