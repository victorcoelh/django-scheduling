from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User

from api.utils.constants import POSSIBLE_TASK_STATUS


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=400)
    date = models.DateField()
    status = models.CharField(choices=POSSIBLE_TASK_STATUS)
    tags = models.ManyToManyField("Tag", through="TaskTag")
    created_on = models.DateField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["owner", "title", "date"], name="unique_task")
        ]
