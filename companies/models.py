import uuid
from django.db import models

class Company(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    basic_cnpj = models.CharField(unique=True)
    company_name = models.CharField()
    legal_nature = models.CharField()
    qualification_of_the_person_in_charge = models.CharField()
    share_company_capital = models.CharField()
    company_size = models.CharField()
    federal_entity_responsible = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_federal_revenue'

    def __str__(self):
        return f'name: {self.name}'