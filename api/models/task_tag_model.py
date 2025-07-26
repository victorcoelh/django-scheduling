from django.db import models

from api.models.tag_model import Tag
from api.models.task_model import Task


class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, to_field="name", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("task", "tag")
