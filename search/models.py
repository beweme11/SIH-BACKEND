from django.db import models
import uuid

class GlobalRegistry(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.TextField()  # No max length

    def __str__(self):
        return self.file_name


class NerData(models.Model):
    uuid = models.ForeignKey(GlobalRegistry, on_delete=models.CASCADE, related_name='ner_data')
    case_number = models.TextField(null=True, blank=True)  # Comma-separated string
    court = models.TextField(null=True, blank=True)
    date = models.TextField(null=True, blank=True)  # Use TextField to allow flexibility
    gpe = models.TextField(null=True, blank=True)  # Geopolitical entities
    judge = models.TextField(null=True, blank=True)
    lawyer = models.TextField(null=True, blank=True)
    org = models.TextField(null=True, blank=True)
    other_person = models.TextField(null=True, blank=True)
    petitioner = models.TextField(null=True, blank=True)
    precedent = models.TextField(null=True, blank=True)
    provision = models.TextField(null=True, blank=True)
    respondent = models.TextField(null=True, blank=True)
    statute = models.TextField(null=True, blank=True)
    witness = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"NerData for UUID: {self.uuid}"


class SummaryData(models.Model):
    uuid = models.ForeignKey(GlobalRegistry, on_delete=models.CASCADE, related_name='summary_data')
    summary = models.TextField()  # TextField for the summary content
    file_name = models.TextField()  # No max length for file name

    def __str__(self):
        return f"SummaryData for {self.file_name}"
