from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=40, primary_key=True)
    icon = models.ImageField(upload_to="assets/icons/")
    created_on = models.DateField(auto_now=True)
