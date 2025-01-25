from django.db import models
from upload.validators.image_validators import validate_image
import os

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/' ,verbose_name='Image', validators=[validate_image])
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name= 'Uploaded at')
    
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        db_table = 'images'
        managed = True
        ordering = ['uploaded_at']
          
    def __str__(self):
        return self.image.name
    
    def delete(self, *args, **kwargs):
        """
        Overrides the model's delete method to perform additional cleanup.

        This method is executed every time an instance of the model is deleted
        individually, whether from the Django admin, a view, or any other location
        where the delete() method is explicitly called.

        Functionality:
        - Physically deletes the associated file from the file system before
          removing the database record.

        Warning:
        - This method is not executed during bulk deletions performed with
          QuerySet.delete(), as these operations bypass the instance's delete()
          method.

        Parameters:
        - *args, **kwargs: Additional arguments that may be passed to the
          delete() method.

        Example:
        >>> instance = Image.objects.get(pk=1)
        >>> instance.delete()  # Deletes the record and its associated file
        """
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    