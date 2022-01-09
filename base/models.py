from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

# Basic model for storing invoice related information
class Invoice(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    
    invoiceNumber = models.CharField(max_length=200, null=False, blank=False, unique=True)
    file = models.FileField(null=False, blank=False, validators=[FileExtensionValidator(['pdf'])])
    vendor = models.TextField(null=True, blank=True)
    buyer = models.TextField(null=True, blank=True)
    billedAmt = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    billedDate = models.DateTimeField(null=True, blank=True)
    items = models.TextField(null=True, blank=True)
    isDigitized = models.BooleanField(null=False, blank=False, default=False)

    created_timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return "{}:{}".format(self._id, self.invoiceNumber)
        
    
