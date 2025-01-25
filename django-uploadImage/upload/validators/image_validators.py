from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image as PILImage

def validate_image(image):
    # Comprobar el tamaño máximo (en bytes, aquí 2 MB)
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError(_("Image size should not exceed 2 MB."))

    # Comprobar los formatos permitidos
    valid_formats = ['JPEG', 'PNG', 'GIF']
    try:
        img = PILImage.open(image)
        if img.format not in valid_formats:
            raise ValidationError(_("Unsupported image format. Allowed formats: JPEG, PNG, GIF."))
    except Exception as e:
        raise ValidationError(_("Invalid image file."))