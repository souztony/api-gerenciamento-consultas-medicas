from rest_framework import viewsets, permissions
from .models import Professional
from .serializers import ProfessionalSerializer

class ProfessionalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualização e edição de profissionais de saúde.
    """
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    # permission_classes = [permissions.AllowAny] # Removido para seguir configuração global (IsAuthenticated)
