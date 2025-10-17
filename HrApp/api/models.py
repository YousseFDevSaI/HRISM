from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100)
    date_uploaded_in = models.CharField(max_length=255, null=True, blank=True)
    approved_by = models.CharField(max_length=255, null=True, blank=True)
    empty_field_a = models.CharField(max_length=255, null=True, blank=True)
    empty_field_b = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.approved_by:
            self.approved_by = []  # Initialize approved_by as an empty list if it's not set
        super().save(*args, **kwargs)
    
class Log(models.Model):
    action = models.CharField(max_length=2500)
    file_name = models.CharField(max_length=2500)
    empty_field_a = models.CharField(max_length=255, null=True, blank=True)
    empty_field_b = models.CharField(max_length=255, null=True, blank=True)
    empty_field_c = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.action

class Flow(models.Model):
    
    service = models.CharField(max_length=100)
    parties_concerned = models.CharField(max_length=1500)
    empty_field_a = models.CharField(max_length=255, null=True, blank=True)
    empty_field_b = models.CharField(max_length=255, null=True, blank=True)
    empty_field_c = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.service
    
class User(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=1500)
    department = models.CharField(max_length=100)
    empty_field_a = models.CharField(max_length=255, null=True, blank=True)
    empty_field_b = models.CharField(max_length=255, null=True, blank=True)
    empty_field_c = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} in department {self.department}"
    
class Dimesnsion(models.Model):
    
    attribute_name = models.CharField(max_length=100)
    row_attribute = models.CharField(max_length=100, null=True, blank=True)
    empty_field_a = models.CharField(max_length=255, null=True, blank=True)
    empty_field_b = models.CharField(max_length=255, null=True, blank=True)
    empty_field_c = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.attribute_name