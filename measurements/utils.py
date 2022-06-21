# from django.contrib.gis.geoip2 import GeoIP2
# from django.contrib.gis.geoip import GeoIP
import requests
import json
import polyline

# Helper functions

def routing(a,b):
    route_url='http://router.project-osrm.org/route/v1/driving/a[0],a[1];b[0],b[1]?alternatives=true&geometries=polyline'
    r=requests.get(route_url)
    res=r.json()
    print(res)
    return res

def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://router.project-osrm.org/route/v1/driving/"
    r = requests.get(url + loc) 
    if r.status_code!= 200:
        return {}
    res = r.json()   
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']
    
    out = {
           'route':routes,
           'start_point':start_point,
           'end_point':end_point,
           'distance':distance
          }

    return out

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def get_geo(ip):
#     g = GeoIP2()
#     country = g.country(ip)
#     city = g.city(ip)
#     lat, lon = g.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            lat_lon(ip)
#     return country, city, lat, lon

def get_center_coordinates(latA, longA, latB=None, longB=None):
    cord = (latA, longA)
    if latB:
        cord = [(latA+latB)/2, (longA+longB)/2]
    return cord

def get_zoom(distance):
    if distance <=100:
        return 8
    elif distance > 100 and distance <= 5000:
        return 4
    else:
        return 2