
from django import forms
from .models import Post, Comment, Category, User, Author
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# translation function
from django.utils.translation import gettext_lazy as _ # gettext_lazy works only, gettext doesn't!!!

class PostForm(forms.ModelForm):

    class Meta:

        model = Post

        fields = [
                  # 'author',
                  ('topic'),
                  ('content'),
                  ('contentType'),
                  ('postCategory'),
              ]
              
        labels = {
            'topic': _('Topic'),
            'content': _('Content'),
            'contentType': _('ContentType'),
            'postCategory': _('PostCategory'),
        }

    # widgets = {
    #     'author': forms.HiddenInput(),
    # }
    def clean(self):
        cleaned_data = super().clean()
        topic = cleaned_data.get("topic")
        if topic is not None and len(topic) < 5:
            raise ValidationError({
                "topic": "Описание не может быть менее 5 символов."
            })
        content = cleaned_data.get("content")
        if content == topic:
            raise ValidationError(
                "Content and topic are the same. Please correct!"
            )

        return cleaned_data

    # FIXME: doesn't work!!!
    def clean_name(self):
        topic = self.cleaned_data["topic"]
        if topic[0].islower():
            raise ValidationError(
                "'Topic' has to have the first capital letter"
            )

        return topic

# # comments create
# class CommentForm(forms.ModelForm):

#     class Meta:

#         model = Comment

#         fields = [
#                   ('text'),
#               ]