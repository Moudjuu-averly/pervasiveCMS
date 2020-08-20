from django import forms
from flock.models import Post, Comments
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class HomeForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write a post...'
        }
    ))
    post_image = forms.FileField(widget=forms.FileInput(
         attrs={
             'class': 'form-control',
             'name': 'post_image',
             'type': 'file',
             'placeholder': 'Image',
             'data-validation':'required',
             'data-validation-help':'Upload a an image please.'
         }
     ))
    content = forms.CharField(widget=CKEditorUploadingWidget())

    # post_video = forms.FileField(widget=forms.FileInput(
    #     attrs={
    #         'class': 'form-control'
    #     }
    # ))

    class Meta:
        model = Post
        fields = (
        "title",
        'content',
        'post_image',
        #'post_video',

        )


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Comment...'
        }
    ))
    # comment_image = forms.FileField(widget=forms.FileInput(
    #      attrs={
    #          'class': 'form-control'
    #      }
    #  ))
    # comment_video = forms.FileField(widget=forms.FileInput(
    #     attrs={
    #         'class': 'form-control'
    #     }
    # ))

    class Meta:
        model = Comments
        exclude = (
            'post',
        )
        fields = (
        "text",
        #'post',
        #'comment_image',
        #'comment_video',

        )
