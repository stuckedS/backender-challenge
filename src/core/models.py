from django.db import models
from django.utils import timezone
import uuid

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None, # noqa
    ) -> None:
        # https://docs.djangoproject.com/en/5.1/ref/models/fields/#django.db.models.DateField.auto_now
        self.updated_at = timezone.now()

        if isinstance(update_fields, list):
            update_fields.append('updated_at')
        elif isinstance(update_fields, set):
            update_fields.add('updated_at')

        super().save(force_insert, force_update, using, update_fields)

class Outbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_type = models.CharField(max_length=255)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["processed"]),
        ]
        ordering = ["created_at"]
