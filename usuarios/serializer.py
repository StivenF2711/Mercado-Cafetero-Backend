from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.password_validation import validate_password

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = Usuario
        fields = ['id', 'correo', 'nombre_completo', 'fecha_registro', 'es_activo', 'rol', 'password']

    def validate(self, data):
        # Validar que no exista un usuario con ese correo/username
        correo = data.get('correo')
        if correo and Usuario.objects.filter(username=correo).exists():
            raise serializers.ValidationError({"correo": "Ya existe un usuario con ese correo."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['username'] = validated_data['correo']  # clave para que AbstractUser no falle
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user
