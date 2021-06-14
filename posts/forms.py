from django.forms import ModelForm, forms, Textarea

from .models import Post, Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': "Комментарий"}
        widgets = {
            'text': Textarea(attrs={'rows': 2}),
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Поле обязательно для заполнения')
        return data


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError("Поле обязательно для заполнения")
        return data
