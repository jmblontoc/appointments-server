from .serializers import AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from django.http import Http404
from .validations import is_valid_appointment_date
from .messages import OVERLAP_ERROR, UNAVAILABLE_DATE_ERROR

# Create your views here.


class AppointmentList(APIView):

    def get(self, request):

        # handle filter here
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            appointments = Appointment.filter_by_daterange(
                start_date, end_date)
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)

        appointments = Appointment.get_appointments_json()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            incoming_obj = request.data

            if Appointment.has_conflict(incoming_obj):
                response_data = {
                    'error': OVERLAP_ERROR
                }

                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if not is_valid_appointment_date(incoming_obj):
                response_data = {
                    'error': UNAVAILABLE_DATE_ERROR
                }

                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            response_data = {
                'appointments': Appointment.get_appointments_json()
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetail(APIView):

    def get(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)
        except Appointment.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk).delete()
            response_data = {
                'appointments': Appointment.get_appointments_json()
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment, data=request.data)

            if serializer.is_valid():

                incoming_obj = request.data

                if Appointment.has_conflict_edit(incoming_obj, pk):
                    response_data = {
                        'error': OVERLAP_ERROR
                    }

                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                if not is_valid_appointment_date(incoming_obj):
                    response_data = {
                        'error': UNAVAILABLE_DATE_ERROR
                    }

                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()

                response_data = {
                    'appointments': Appointment.get_appointments_json()
                }

            return Response(response_data, status=status.HTTP_202_ACCEPTED)
        except Appointment.DoesNotExist:
            raise Http404
