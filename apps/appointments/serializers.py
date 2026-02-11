from rest_framework import serializers
from .models import Appointment
from apps.professionals.serializers import ProfessionalSerializer
from django.utils import timezone

class AppointmentSerializer(serializers.ModelSerializer):
    professional_detail = ProfessionalSerializer(source='professional', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'professional', 'professional_detail', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_date(self, value):
        """Validate that appointment date is in the future."""
        if value < timezone.now():
            raise serializers.ValidationError(
                "A data da consulta deve ser no futuro."
            )
        return value
    
    def validate_professional(self, value):
        """Validate that professional exists and is active."""
        if not value:
            raise serializers.ValidationError("O profissional é obrigatório.")
        return value
