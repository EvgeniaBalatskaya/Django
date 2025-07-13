from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def resize_image(image_field):
    target_size = 2000  # желаемая ширина и высота

    img = Image.open(image_field)
    width, height = img.size

    # Вычисляем сторону квадрата для обрезки (минимум из ширины и высоты)
    new_edge = min(width, height)

    # Координаты для центрированной обрезки квадрата
    left = (width - new_edge) // 2
    top = (height - new_edge) // 2
    right = left + new_edge
    bottom = top + new_edge

    # Обрезаем картинку до квадрата
    img_cropped = img.crop((left, top, right, bottom))

    # Масштабируем до 2000x2000
    img_resized = img_cropped.resize((target_size, target_size), Image.LANCZOS)

    # Сохраняем в буфер
    buffer = BytesIO()
    # Чтобы сохранить формат, используем исходный формат, но если его нет, сохраняем в PNG
    img_format = img.format if img.format else 'PNG'
    img_resized.save(buffer, format=img_format)
    buffer.seek(0)

    # Возвращаем Django ContentFile с оригинальным именем файла
    return ContentFile(buffer.read(), name=image_field.name)
