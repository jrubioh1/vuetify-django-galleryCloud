
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from request_casting import request_casting
from django.http import FileResponse, HttpResponse, JsonResponse
from django.db.models import Count, F
from upload.models import Image
from upload.helpers.helpers import get_language
import locale
import calendar 
import os
import io
import zipfile


# @api_view(['GET', 'POST'])
# def my_view(request):
#     if request.method == 'GET':
#         return Response({"message": "This is a GET request"})
#     elif request.method == 'POST':
#         return Response({"message": "This is a POST request"})
#         return Response({"message": "This is a POST request"})
#         return Response({"message": "This is a POST request"})


@api_view(['GET'])
def get_images_by_year_month(request):
    class CustomPagination(PageNumberPagination):
        page_size = 20  # Número de registros por página
        page_size_query_param = 'page_size'

    try:
        get_language(request)
        # Obtener los parámetros year y month como cadenas
        year = request_casting.RequestString(request, 'year', default=None)
        month = request_casting.RequestString(request, 'month', default=None)

        # Validar el valor de year
        if year and not year.isdigit():
            return Response({"message": "Invalid year format. It must be numeric."}, status=400)
        if year:
            year = int(year)
            if year < 1900 or year > 2100:
                return Response({"message": "Invalid year value"}, status=400)

        # Validar y convertir el valor de month
        if month:
            month = month.capitalize()  # Asegura que el nombre del mes sea capitalizado
            month_to_number = {name: index for index, name in enumerate(calendar.month_name) if name}
            if month not in month_to_number:
                return Response({"message": f"Invalid month value: {month}. It must be a valid month name."}, status=400)
            month = month_to_number[month]

        # Consulta base
        images = Image.objects.all().order_by('-uploaded_at')

        # Aplicar filtros si se proporcionan year y month
        if year:
            images = images.filter(uploaded_at__year=year)
        if month:
            images = images.filter(uploaded_at__month=month)

        # Aplicar paginación
        paginator = CustomPagination()
        paginated_images = paginator.paginate_queryset(images, request)

        # Agrupar imágenes por año y mes
        grouped_images = {}
        for image in paginated_images:
            image_year = image.uploaded_at.year
            image_month = calendar.month_name[image.uploaded_at.month]
            if image_year not in grouped_images:
                grouped_images[image_year] = {}
            if image_month not in grouped_images[image_year]:
                grouped_images[image_year][image_month] = []
            grouped_images[image_year][image_month].append({
                "id": image.pk,
                "name": os.path.basename(image.image.url),
                "uploaded_at": image.uploaded_at,
                "url": request.build_absolute_uri(image.image.url),
            })

        # Retornar la respuesta paginada
        return paginator.get_paginated_response(grouped_images)

    except Exception as e:
        return Response({"message": "Error fetching images", "exception": str(e)}, status=500)
    finally:
        # Restaurar el locale predeterminado
        locale.setlocale(locale.LC_TIME, 'C')  # R
@api_view(['GET'])
def get_available_years_and_months(request):
    try:
        get_language(request)
        # Agrupar por años y meses únicos
        grouped_years_months = {}
        years = Image.objects.all().order_by('-uploaded_at__year').distinct().values_list('uploaded_at__year', flat=True)
        for year in years:
            grouped_years_months[year] = []
            months = Image.objects.filter(uploaded_at__year=year).order_by('-uploaded_at__month').distinct().values_list('uploaded_at__month', flat=True)
            for month in months:
                grouped_years_months[year].append(calendar.month_name[month])  # Formato MM

        # Responder con el diccionario
        return Response(grouped_years_months, status=200)

    except Exception as e:
        print(e)
        return Response({"message": "Error fetching years and months", "exception": str(e)}, status=500)
    finally:
        # Restaurar el locale predeterminado
        locale.setlocale(locale.LC_TIME, 'C')  # R
@api_view(['POST'])
def upload_image(request):
    upload_images= request.FILES.getlist( 'image')
    if upload_images is None or len (upload_images)==0:
        return Response({"message": "No image/s uploaded"},400)
        
    try:
        for image in upload_images:
            if not image.content_type.startswith('image/'):
                return Response({"message": f"{image.name} is not a valid image."}, status=400)
            Image.objects.create(image=image)
        
        return Response({"message": "Images uploaded successfully"}, 200)
    except ValidationError as e:
        return Response({"message": "Error uploading image, no match with the requeriments", "exception": e}, 400)
    except Exception as e:
        return Response({"message": "Error uploading image", "exception": e}, 500)

    
@api_view(['GET'])
def download_image(request):
        id_image = request_casting.RequestInteger(request, 'id', default=None)
        
        if id_image is None:
            return Response({"message": "No id image"},400)
        try:
            image= Image.objects.get(id=id_image)
            return FileResponse(open(image.image.path, 'rb'), 200)
        
        except Image.DoesNotExist:
            return Response({"message": "Image not found"}, 404)
        except Exception as e:  
            return Response({"message": "Error downloading image", "exception": e}, 500)
        
@api_view(['GET'])
def download_images(request):
    try:
        # Obtener todas las imágenes
        images = Image.objects.all()

        # Agrupar imágenes por año y mes
        grouped_images = {}
        for image in images:
            uploaded_at = image.uploaded_at
            year = uploaded_at.year
            month = f"{uploaded_at.month:02}"  # Asegura que el mes tenga 2 dígitos

            if year not in grouped_images:
                grouped_images[year] = {}

            if month not in grouped_images[year]:
                grouped_images[year][month] = []

            grouped_images[year][month].append({
                "id": image.pk,
                "name": os.path.basename(image.image.url),
                "uploaded_at": uploaded_at,
                "url": request.build_absolute_uri(image.image.url),
            })

        # Devolver las imágenes agrupadas por año y mes
        return Response(grouped_images, status=200)

    except Exception as e:
        return Response({"message": "Error downloading images", "exception": str(e)}, status=500)



@api_view(['POST'])
def download_selected(request):
        selected= request.data.getlist('id')
        print(selected, "selected")
        
        if selected is None or len(selected)==0:
            return Response({"message": "No image/s selected"},400)
        
        try:
            images= Image.objects.filter(id__in=selected)
            if not images.exists():
                return Response({"message": "No images found"}, 404)
        
            # Crear un archivo ZIP en memoria
            zip_filename = "selected_images.zip"
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for image in images:
                    # Agregar cada archivo de imagen al ZIP
                    zip_file.write(image.image.path, os.path.basename(image.image.path))
            
            zip_buffer.seek(0)  # Volver al inicio del archivo ZIP en memoria

            # Preparar la respuesta HTTP con el archivo ZIP
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={zip_filename}'
            return response
        
        except Image.DoesNotExist:
            return Response({"message": "Image not found"}, 404)
        except Exception as e:  
            return Response({"message": "Error downloading image", "exception": e}, 500)
        
@api_view(['DELETE'])
def delete_image(request):
        id_image = request_casting.RequestInteger(request, 'id', default=None)
    
        
        if id_image is None:
            return Response({"message": "No id image"},400)
    

        try:
            Image.objects.get(id=id_image).delete()
        
            return Response({"message": "Image deleted successfully"}, 200)
        
        except Image.DoesNotExist:
            return Response({"message": "Image not found"}, 404)
        except Exception as e:  
            return Response({"message": "Error downloading image", "exception": e}, 500)

@api_view(['DELETE'])
def delete_selected(request):
        selected= request.data.getlist('id')
        print(selected, "selected")
        
        if selected is None or len(selected)==0:
            return Response({"message": "No image/s selected"},400)
        
        try:
            Image.objects.filter(id__in=selected).delete()
            
        
            return Response({"message": "Image deleted successfully"}, 200)
        
        except Image.DoesNotExist:
            return Response({"message": "Image not found"}, 404)
        except Exception as e:  
            return Response({"message": "Error downloading image", "exception": e}, 500)
@api_view(['GET'])
def photos_tree_staistics(request):
    # Consultar y agrupar las fotos por año y mes
    get_language(request)
    photos_data = Image.objects.annotate(
        year=F('uploaded_at__year'),
        month=F('uploaded_at__month')
    ).values('year', 'month').annotate(
        count=Count('id')
    ).order_by('year', 'month')

    # Crear la estructura jerárquica
    data = []
    years = {}

    for item in photos_data:
        year = item['year']
        month = item['month']
        count = item['count']

        if year not in years:
            years[year] = {'name': str(year), 'children': []}

        years[year]['children'].append({
            'name': calendar.month_name[month],
            'value': count
        })

    data = list(years.values())
    locale.setlocale(locale.LC_TIME, 'C')  
    
    return JsonResponse(data, safe=False)