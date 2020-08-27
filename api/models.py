from django.db import models
from .validations import is_conflict
from datetime import datetime
# Create your models here.


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    comments = models.TextField(null=True, blank=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'comments': self.comments
        }

    @staticmethod
    def get_appointments_json():
        return [item.to_json() for item in Appointment.objects.order_by('from_date')]

    @staticmethod
    def has_conflict(appointment):
        for entry in Appointment.objects.all():
            if is_conflict(appointment, entry):
                return True
        return False

    @staticmethod
    def has_conflict_edit(appointment, id):
        for entry in Appointment.objects.all():
            if is_conflict(appointment, entry) and id != entry.id:
                return True
        return False

    @staticmethod
    def filter_by_daterange(start_date, end_date):
        format = '%Y-%m-%d'

        s_date = datetime.strptime(start_date, format).date()
        e_date = datetime.strptime(end_date, format).date()

        return [item.to_json() for item in Appointment.objects.all() if s_date <= item.from_date.date() <= e_date]
