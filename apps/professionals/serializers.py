from rest_framework import serializers
from .models import Professional
import re

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['id', 'social_name', 'profession', 'address', 'contact', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_social_name(self, value):
        """Validate and sanitize social name."""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome social não pode estar vazio.")
        
        # Remove caracteres especiais perigosos (XSS prevention)
        sanitized = value.strip()
        if len(sanitized) < 3:
            raise serializers.ValidationError("O nome social deve ter pelo menos 3 caracteres.")
        if len(sanitized) > 200:
            raise serializers.ValidationError("O nome social não pode exceder 200 caracteres.")
        
        return sanitized
    
    def validate_profession(self, value):
        """Validate profession field."""
        if not value or not value.strip():
            raise serializers.ValidationError("A profissão não pode estar vazia.")
        
        sanitized = value.strip()
        if len(sanitized) < 3:
            raise serializers.ValidationError("A profissão deve ter pelo menos 3 caracteres.")
        
        return sanitized
    
    def validate_contact(self, value):
        """Validate contact information."""
        if not value or not value.strip():
            raise serializers.ValidationError("O contato não pode estar vazio.")
        
        sanitized = value.strip()
        
        # Basic email or phone validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
        
        if not (re.match(email_pattern, sanitized) or re.match(phone_pattern, sanitized)):
            raise serializers.ValidationError(
                "O contato deve ser um email válido ou telefone no formato (XX) XXXXX-XXXX."
            )
        
        return sanitized
