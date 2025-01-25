
from upload import views
from django.urls import path

urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
    path('download_image/', views.download_image, name='download_image'),
    path('download_images/', views.download_images, name='download_images'),
    path('delete_image/', views.delete_image, name='delete_image'),
    path('delete/', views.delete_selected, name='delete_selected'),
    path('download_selected/', views.download_selected, name='download_selected'),
    path('get_images_by_year_month/', views.get_images_by_year_month, name='get_images_by_year_month'),
    path('get_available_years_and_months/', views.get_available_years_and_months, name='get_available_years_and_months'),
    path('photos_tree_staistics/', views.photos_tree_staistics, name='photos_tree_staistics'),
   
    
]