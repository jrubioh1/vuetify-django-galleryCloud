from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Image
import os

@receiver(pre_save, sender=Image)
def delete_old_file(sender, instance, **kwargs):
    """
    Pre-save signal to handle the deletion of old files associated with a model.

    This signal is triggered automatically before saving an instance of the
    `Image` model. Its main purpose is to prevent orphaned files in the file system
    when an image is updated.

    Functionality:
    - Detects if the instance already exists in the database.
    - Compares the current image file with the new file.
    - If the files are different, it physically deletes the old file from the
      file system.

    Warning:
    - Does not delete files if the object is new (without a primary key assigned).
    - Ensure that the file paths are correct and accessible.

    Parameters:
    - sender: The model class sending the signal (`Image` in this case).
    - instance: The specific instance being saved.
    - **kwargs: Additional arguments provided by the signal.

    Example:
    >>> instance = Image.objects.get(pk=1)
    >>> instance.image = 'images/new_image.jpg'
    >>> instance.save()  # The signal automatically deletes the old file
    """
    if not instance.pk:
        return  # Si es un objeto nuevo, no se hace nada

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return

    # Compara el archivo actual con el nuevo
    if old_file and old_file != instance.image:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
            
@receiver(pre_delete, sender=Image)
def call_delete_on_bulk_delete(sender, instance, **kwargs):
    """
    Ensures the delete() method is called on each instance during bulk deletions.

    This signal is triggered before a record is deleted from the database,
    including during bulk deletions.
    """
    # Call the instance's delete() method
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)