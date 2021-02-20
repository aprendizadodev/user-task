from django.db import models

class User(models.Model):
    class Meta:
        db_table = "user"
        managed = True
    name = models.CharField(max_length=200, blank=False, default='')


class Task(models.Model):
    class Meta:
        db_table = "task"
        managed = True
    description = models.CharField(max_length=200, blank=False, default='')
    state = models.BooleanField(null=True)
    user_id = models.ForeignKey("User", db_column="user_id", db_index=True,
                                blank=True, null=True, db_constraint=True, on_delete=models.PROTECT)
