from django import forms

from audio_surveys.models import AudioSet


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            # print(data)
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class AudioSetModelForm(forms.ModelForm):
    audio_examples = MultipleFileField(label="Audio Examples", required=True)

    class Meta:
        model = AudioSet
        fields = ["audio_examples", "name"]


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()
    name = forms.CharField()


class AudioSetForm(forms.BaseModelForm):
    form = FileFieldForm()
