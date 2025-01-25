from django.core.exceptions import ValidationError

class AlphanumericWithSpecialCharValidator:
    """
    Validador de contraseñas personalizado para asegurar un nivel mínimo de complejidad.

    Este validador garantiza que las contraseñas cumplan con los siguientes requisitos:
        - Longitud mínima de 8 caracteres.
        - Contienen al menos un número.
        - Contienen al menos una letra.
        - Contienen al menos un carácter especial (!@#$%^&*()-_=+[]{};:,.<>?/|).

    **Configuración en settings.py:**
    Para usar este validador en toda la aplicación, agrégalo a la lista `AUTH_PASSWORD_VALIDATORS`:
    
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 8,  # Opcional, ya se valida en este validador
            },
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
        {
            'NAME': 'authJWT.validators.validator_password.AlphanumericWithSpecialCharValidator',
        },
    ]

    **Uso automático:**
    - Cuando se configura en `AUTH_PASSWORD_VALIDATORS`, este validador se aplicará automáticamente en los formularios predeterminados de Django, como:
        - Cambio de contraseña (`PasswordChangeForm`).
        - Restablecimiento de contraseña (`SetPasswordForm`).

    **Uso en vistas personalizadas:**
    - Para aplicar este validador manualmente en vistas personalizadas, utiliza la función `validate_password` de Django:
        from django.contrib.auth.password_validation import validate_password

        try:
            validate_password(password)  # Aplica todos los validadores configurados en settings.py
        except ValidationError as e:
            return Response({"error": e.messages}, status=400)

    **Por qué implementarlo:**
    - Este validador mejora la seguridad de las contraseñas al exigir un nivel básico de complejidad.
    - Protege contra ataques de fuerza bruta y minimiza el uso de contraseñas débiles.
    - Permite centralizar las reglas de validación, garantizando consistencia en toda la aplicación.

    """
    def validate(self, password, user=None):
        # Longitud mínima
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        # Al menos un número
        if not any(char.isdigit() for char in password):
            raise ValidationError("La contraseña debe contener al menos un número.")
        # Al menos una letra
        if not any(char.isalpha() for char in password):
            raise ValidationError("La contraseña debe contener al menos una letra.")
        # Al menos un carácter especial
        if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/|" for char in password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial (!@#$%^&*()-_=+[]{};:,.<>?/|).")

    def get_help_text(self):
        return "Tu contraseña debe contener al menos 8 caracteres, incluyendo letras, números y un carácter especial (!@#$%^&*()-_=+[]{};:,.<>?/|)."