from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework.response import Response
from django.http import FileResponse, HttpResponse, JsonResponse
from django.db.models import Count, F
from request_casting import request_casting
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from authJWT.validators.validator_password import AlphanumericWithSpecialCharValidator

@api_view(['POST'])

@api_view(['POST'])
def register(request):
        username = request_casting.RequestString(request, 'username', None)
        password = request_casting.RequestString(request,'password',  None)
        mail = request_casting.RequestString(request,'mail',  None)

        
            # Verificar que los campos estén presentes
        if not username or not password:
            return Response({"error": "Todos los campos son obligatorios."}, status=400)

        # Validar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe."}, status=400)

        try:
            # Aplicar validadores de contraseña configurados en settings.py
            validate_password(password)
            
            # Aplicar validador personalizado
            custom_validator = AlphanumericWithSpecialCharValidator()
            custom_validator.validate(password)

        except ValidationError as e:
            # Capturar y enviar los mensajes de error de validación
            return Response({"error": e.messages}, status=400)

        # Crear el usuario con la contraseña cifrada
        user = User.objects.create(
            username=username,
            password=make_password(password), # Guardar la contraseña cifrada
            mail=mail
        )

        return Response({"message": "Usuario registrado correctamente."}, status=201)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request_casting.RequestString(request,"refresh", None)  # Obtén el token de refresh desde el body
        if not refresh_token:
            return Response({"error": "El token de refresh es obligatorio."}, status=400)
        
        # Busca el token en OutstandingToken y lo pone en la lista negra
        token = OutstandingToken.objects.get(token=refresh_token)
        BlacklistedToken.objects.create(token=token)
        return Response({"message": "Cierre de sesión exitoso."}, status=200)
    except OutstandingToken.DoesNotExist:
        return Response({"error": "Token de refresh no válido."}, status=400)
    except Exception as e:
        return Response({"error": "Ocurrió un error al intentar cerrar sesión."}, status=500) 