import uuid
from django.db import models

class State(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    api_id = models.IntegerField(unique=True)
    acronym = models.CharField()
    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'state_ibge'

    def __str__(self):
        return f'name: {self.name}'
