import uuid
from django.db import models

class State(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    integration_id = models.IntegerField()
    acronym = models.CharField()
    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'state_ibge'