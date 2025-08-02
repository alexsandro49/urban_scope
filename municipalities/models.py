import uuid
from django.db import models
from states.models import State

class Municipality(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    api_id = models.IntegerField(unique=True)
    name = models.CharField()
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'municipality_ibge'

    def __str__(self):
        return f'name: {self.name}'