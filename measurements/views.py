from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_center_coordinates, get_zoom,routing,get_route
import folium
import geocoder
import requests
import polyline

# Create your views here.

def calculate_distance_view(request):
    # initial values
    distance = None
    destination = None
    temperatureA = None
    descriptionA = None
    iconA = None
    temperatureB = None
    descriptionB = None
    iconB = None
    cityB =""
    cityA =""
    
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')
    obg_s = Measurement.objects.all().last()
    address = obg_s.address
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    # Create Map Object
    m = folium.Map(location=[19, -12], zoom_start=2)

    # S
    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        address = form.cleaned_data.get('address')
        location = geocoder.osm(address)
        lat = location.lat
        lng = location.lng
        country = location.country
        cityA = location.city
        if lat == None or lng == None:
            address.delete()
            return HttpResponse('You address input is invalid')

        # location coordinates
        l_lat = lat
        l_lon = lng
        pointA = (l_lat, l_lon)

        # initial folium map
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=country,
                        icon=folium.Icon(color='purple')).add_to(m)

        # destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        # cityB = destination.city
        pointB = (d_lat, d_lon)
        # distance calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=country,
                    icon=folium.Icon(color='purple')).add_to(m)
        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(m)


        l_lon,l_lat,d_lon,d_lat = float(l_lon),float(l_lat),float(d_lon),float(d_lat)
        route=get_route(l_lon,l_lat,d_lon,d_lat)
        
        # drow the route betwen two locations
        folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
        # m.add_child(r)

        # # draw the line between location and destination
        # line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        # m.add_child(line)

        # weather api point A
        cityA = address
        api_urlA = "http://api.openweathermap.org./data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
        urlA = api_urlA + cityA
        responseA = requests.get(urlA)
        contentA = responseA.json() 
        temperatureA = contentA['main']['temp']
        descriptionA = contentA['weather'][0]['description']
        iconA = contentA['weather'][0]['icon']
        # weather api point B
        cityB = destination_
        api_urlB = "http://api.openweathermap.org./data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
        urlB = api_urlB + cityB
        responseB = requests.get(urlB)
        contentB = responseB.json() 
        temperatureB = contentB['main']['temp']
        descriptionB = contentB['weather'][0]['description']
        iconB = contentB['weather'][0]['icon']
        
        instance.location = location
        instance.distance = distance
        instance.save()
    
    m = m._repr_html_()
    

    context = {
        'distance' : distance,
        'destination': destination,
        'form': form,
        'map': m,
        'address': address,
        # 'city': address,
        'Rosso' : cityB,
        'kiffa' : cityA,
        'temperatureA': temperatureA,
        'descriptionA' : descriptionA,
        'iconA' : iconA,
        'temperatureB': temperatureB,
        'descriptionB' : descriptionB,
        'iconB' : iconB
    }

    return render(request, 'measurements/main.html', context)

def drow_object(request):
    return render(request, 'measurements/draw.html')