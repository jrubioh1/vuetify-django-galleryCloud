import locale
def get_language(request):  
    # Obtener idioma desde los headers
        accept_language = request.headers.get('Accept-Language', 'en')  # Valor predeterminado: inglés
        language_map = {
            'es': 'es_ES.UTF-8',  # Español
            'en': 'en_US.UTF-8',  # Inglés
        }
        locale_name = language_map.get(accept_language.split(',')[0].split('-')[0], 'en_US.UTF-8')

        # Configurar el locale temporalmente
        try:
            locale.setlocale(locale.LC_TIME, locale_name)
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')  # Fallback a inglés si no está disponible
