from .models import Appointment
from rest_framework import serializers


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'name', 'from_date', 'to_date', 'comments']
