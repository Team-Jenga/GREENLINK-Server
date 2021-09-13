from django.db import models

class Main(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        """A string representation of the model."""
        return self.title