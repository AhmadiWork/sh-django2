from django.db import models

from apps.shortener.models import AlmaURL


class ClickEventManager(models.Manager):
    def create_event(self, alma_instance):
        if isinstance(alma_instance, AlmaURL):
            obj, created = self.get_or_create(alma_url=alma_instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    alma_url = models.OneToOneField(AlmaURL, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)
