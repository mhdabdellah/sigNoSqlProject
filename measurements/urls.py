from django.urls import path
from .views import calculate_distance_view,drow_object

app_name = 'measurements'

urlpatterns = [
    path('', calculate_distance_view, name='calaculate-view'),
    path('drow_object', drow_object, name='drow_object'),
]
