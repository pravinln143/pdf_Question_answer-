from django.db import models

class Document(models.Model):
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # Store extracted text here for NLP

    def __str__(self):
        return self.filename