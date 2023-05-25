from django.db import models

class AnnualData(models.Model):
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    field3 = models.IntegerField()
    # Add more fields as needed

    def __str__(self):
        return self.field1
