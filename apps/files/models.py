from django.db import models


class File(models.Model):
    file = models.FileField(upload_to="file/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name}"

    class Meta:
        verbose_name_plural = "Files"
        ordering = ["-created_at"]
