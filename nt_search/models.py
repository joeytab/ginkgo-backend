import os
import sys

sys.path.append(os.path.dirname(__file__))
import json
from django.db import models
import jsonfield
#  from computedfields.models import ComputedFieldsModel, computed, compute
# Create your models here.
class Response(models.Model):
    id = models.AutoField(primary_key = True)
    sequence = models.CharField(max_length = 500)

    def _str_(self):
        return self.sequence


