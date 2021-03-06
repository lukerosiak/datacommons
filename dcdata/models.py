from django.db import models

class Import(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255)
    description = models.TextField()
    imported_by = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('-timestamp',)
    
    def __unicode__(self):
        return self.timestamp.isoformat()

