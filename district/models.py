import uuid
from django.db import models
from states.models import State
from municipalities.models import Municipality

class District(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    api_id = models.IntegerField()
    name = models.CharField()
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'district_ibge'

    def __str__(self):
        return f'name: {self.name}'