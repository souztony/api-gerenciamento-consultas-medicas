from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualização e edição de consultas médicas.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        appointment = serializer.save()
        # Trigger Asaas Mock
        from .services import AsaasService
        AsaasService.create_payment_with_split(appointment)

    def get_queryset(self):
        """
        Opcionalmente filtra as consultas por id do profissional através do parâmetro `professional_id`.
        """
        queryset = Appointment.objects.all()
        professional_id = self.request.query_params.get('professional_id')
        if professional_id is not None:
            queryset = queryset.filter(professional_id=professional_id)
        return queryset
