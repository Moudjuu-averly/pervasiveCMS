from django import forms
from jobs.models import PostJob
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class JobForm(forms.ModelForm):
    job_tittle = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Job tittle...',
            'data-validation':'required',
            'data-validation-help':'Provide a Job Need title.'
        }
    ))
    job_type = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'job_type',
            'selected': '',
            'data-validation':'required',
        }
    ), choices=PostJob.JOB_TYPE_CHOICES
    )
    job_video = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'name': 'job_video',
            'type': 'file',
            'data-validation':'required',
            'data-validation-help':'Upload a video for this job please.'
        }
    )
    )
    due_date = forms.DateField(
        label='Due Date',
        widget=forms.widgets.DateInput(attrs={
        'type':'date',
        'id':'datetimepicker',
        'class':'form-control date-picker',
        'data-datepicker-color':'primary',
        'data-validation':'required',
        'data-validation-help':'Please provide a valid future date.'
         }),
    )
    min_salary = forms.CharField(
        label='Minimun',
        widget=forms.widgets.TextInput(attrs={
        'type':'number',
        'data-validation':'required',
        'class':'form-control input',
        'data-validation-help':'Provide an amount greater than N$ 1500.00.',
        'placeholder': '$1600.00'
         }),
    )
    max_salary = forms.CharField(
        label='Maximun',
        widget=forms.widgets.TextInput(attrs={
        'type':'number',
        'class':'form-control input',
        'placeholder': '$160000.00',
        'data-validation':'required',
        'data-validation-help':'Provide an amount greater in N$ dollars'
         }),
    )#id="editable"
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = PostJob
        fields = (
        'content',
        'job_tittle',
        'job_type',
        'job_video',
        'due_date',
        'max_salary',
        'min_salary',
        )
        exclude = (
        'user',
        'view_by',
        )
    #def clean_image(self):
    #        """ Clean the uploaded image attachemnt.
    #        """
    #        image = self.cleaned_data.get('image', False)
    #        utils.ensure_safe_user_image(image)
    #        return image

class UpdateJobForm(forms.ModelForm):
    job_tittle = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Job tittle...',
            'data-validation':'required',
            'data-validation-help':'Provide a Job Need title.'
        }
    ))
    job_type = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'job_type',
            'selected': '',
            'data-validation':'required',
        }
    ), choices=PostJob.JOB_TYPE_CHOICES
    )
    job_video = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'name': 'job_video',
            'type': 'file',
            'data-validation':'required',
            'data-validation-help':'Upload a video for this job please.'
        }
    )
    )
    due_date = forms.DateField(
        label='Due Date',
        widget=forms.widgets.DateInput(attrs={
        'type':'date',
        'id':'datetimepicker',
        'class':'form-control date-picker',
        'data-datepicker-color':'primary',
        'data-validation':'required',
        'data-validation-help':'Please provide a valid future date.'
         }),
    )
    min_salary = forms.CharField(
        label='Minimun',
        widget=forms.widgets.TextInput(attrs={
        'type':'number',
        'data-validation':'required',
        'class':'form-control input',
        'data-validation-help':'Provide an amount greater than N$ 1500.00.',
        'placeholder': '$1600.00'
         }),
    )
    max_salary = forms.CharField(
        label='Maximun',
        widget=forms.widgets.TextInput(attrs={
        'type':'number',
        'class':'form-control input',
        'placeholder': '$160000.00',
        'data-validation':'required',
        'data-validation-help':'Provide an amount greater in N$ dollars'
         }),
    )


    class Meta:
        model = PostJob
        fields = (
        'content',
        'job_tittle',
        'job_type',
        'job_video',
        'due_date',
        'max_salary',
        'min_salary',
        )
        exclude = (
        'views',
        'deleted',
        )




def ensure_safe_user_image(image):
    """ Perform various checks to sanitize user uploaded image data.

    Checks that image was valid header, then

    :param: InMemoryUploadedFile instance (Django form field value)

    :raise: ValidationError in the case the image content has issues
    """

    if not image:
        return

    assert isinstance(image, InMemoryUploadedFile), "Image rewrite has been only tested on in-memory upload backend"

    # Make sure the image is not too big, so that PIL trashes the server
    if image:
        if image._size > 4*1024*1024:
            raise ValidationError("Image file too large - the limit is 4 megabytes")

    # Then do header peak what the image claims
    image.file.seek(0)
    mime = magic.from_buffer(image.file.getvalue(), mime=True)
    if mime not in ("image/png", "image/jpeg", "image/jpg"):
        raise ValidationError("Image is not valid. Please upload a JPEG or PNG image.")

    doc_type = mime.split("/")[-1].upper()

    # Read data from cStringIO instance
    image.file.seek(0)
    pil_image = Image.open(image.file)

    # Rewrite the image contents in the memory
    # (bails out with exception on bad data)
    buf = StringIO()
    pil_image.thumbnail((2048, 2048), Image.ANTIALIAS)
    pil_image.save(buf, doc_type)
    image.file = buf

    # Make sure the image has valid extension (can't upload .htm image)
    extension = unicode(doc_type.lower())
    if not image.name.endswith(u".%s" % extension):
        image.name = image.name + u"." + extension
