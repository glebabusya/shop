from django import forms
from . import models

CHOICES = [('5', 5), ('4', 4), ('3', 3), ('2', 2), ('1', 1)]


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('comment', 'rating')
        widgets = {

            'rating': forms.Select(choices=CHOICES, attrs={'class': 'comment-input'}),
            'comment': forms.Textarea(attrs={'class': 'comment-input'}),
        }
        labels = {
            'comment': 'Review'

        }
