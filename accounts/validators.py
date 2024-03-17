# here we make custome validator function
import os
from django.core.exceptions import ValidationError

def check_images(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.png','.jpg','.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported valid extension. Allowed Extensions :" + str(valid_extensions))