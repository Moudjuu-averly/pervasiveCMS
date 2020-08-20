from django import forms
from .models import Support


class SupportForm(forms.ModelForm):
    support_tittle          = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'support_tittle', 
            'placeholder': 'Tittle...',
            'type': 'text',
            'data-validation':'required',
        }
    ))

    support_type            = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'support_type',
            'data-validation':'required',
        }
    ), choices=Support.SUPPORT_TYPE_CHOICES
    )
    image                   = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'name': 'image',
            'type': 'file',
        }
    )
    )
    content                 = forms.CharField(required=True, label='About', widget=forms.Textarea(
         attrs={
             'class': 'form-control input-group',
             'name':'content',
             'data-validation':'required',
             'placeholder': 'Lamborghini Mercy, Your chick she so thirsty, I\'m in that two seat Lambo.'
         }
     ))

    class Meta:
        model = Support
        fields = (
        'support_tittle',
        'support_type',
        'image',
        'content',
        )
        exclude = (
        'user',
        'viewed_by_ip',
        'created',
        'seen',
        'seen_by_us',
        'viewed_at',
        )
    #def clean_image(self):
    #    """ Clean the uploaded image attachemnt.
    #    """
    #    image = self.cleaned_data.get('image', False)
    #    ensure_safe_user_image(image)
    #    return image



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
