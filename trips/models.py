from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    def is_completed(self):
        if not self.places.exists():
            return False
        return not self.places.filter(is_visited=False).exists()

    def __str__(self):
        return self.name

class Place(models.Model):
    project = models.ForeignKey(Project, related_name='places', on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('project', 'external_id')

    def __str__(self):
        return f"Place {self.external_id} in {self.project.name}"