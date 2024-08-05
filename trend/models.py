from django.db import models

# Create your models here.
class BrandTrend(models.Model):
    bname = models.CharField(max_length=200)

    def __str__(self):
        return f"Brand Trend: {self.bname}"