from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def resize_image(image_field):
    target_ratio = 2

    img = Image.open(image_field)
    width, height = img.size

    if width / height > target_ratio:
        new_height = height
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        right = left + new_width
        top = 0
        bottom = height
    else:
        new_width = width
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        left = 0
        right = width

    img_cropped = img.crop((left, top, right, bottom))

    buffer = BytesIO()
    img_cropped.save(buffer, format=img.format)
    return ContentFile(buffer.getvalue(), name=image_field.name)
