from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from amadeus import Client, ResponseError, Location
from rest_framework import generics
from .models import Vuelo
from .serializer import SerializerVuelo, SerializerUser
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

amadeus = Client(
    client_id='GoJxdZIivaehEX52UiZVUlGS7Ob0sm6H',
    client_secret='tFOeUaHd2sKASvqd'
)


def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))
    return result


import json

f = open(r'C:\Users\mherr\Desktop\Final Web Proyect\Final_Project_Backend\testdata.json')
data = json.load(f)
# for i, x in data.items():
#     print(i, x)
f.close()


# print()
# print({
#     'salida': data['itineraries'][0]['segments'][0]['departure']['iataCode'],
#     'llegada': data['itineraries'][0]['segments'][0]['arrival']['iataCode'],
#     'tsalida': data['itineraries'][0]['segments'][0]['departure']['at'].partition('T')[2][:-3:],
#     'tllegada': data['itineraries'][0]['segments'][0]['arrival']['at'].partition('T')[2][:-3:],
#     'precio': data['price']['grandTotal'] + ' ' + data['price']['currency']
# })


# Create your views here.
@api_view(["GET"])
def Prueba(request):
    print(request.data)
    return Response({"dd": "d"})


@api_view(["POST"])
def Prueba(request):
    print(request.data)
    return Response({"si": "d"})


@api_view(["POST"])
def flight_options(request):
    t = json.loads(request.data['json1'])
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=t['Salida'],
            destinationLocationCode=t['Llegada'],
            departureDate=t['FechaIda'],
            adults=1)
        t = response.data
        print(t[0])
        dat = []
        for i in t:
            dat.append({
                'salida': i['itineraries'][0]['segments'][0]['departure']['iataCode'],
                'llegada': i['itineraries'][0]['segments'][-1]['arrival']['iataCode'],
                'tsalida': i['itineraries'][0]['segments'][0]['departure']['at'].partition('T')[2][:-3:],
                'tllegada': i['itineraries'][0]['segments'][-1]['arrival']['at'].partition('T')[2][:-3:],
                'precio': i['price']['grandTotal'] + ' ' + i['price']['currency']
            })
        response = response.data[0]
    except ResponseError as error:
        print(error)
    return Response({"data": dat})


@api_view(["POST"])
def airportcode(request):
    try:
        response = amadeus.reference_data.locations.get(keyword=request.data.get("code", " "), subType=Location.ANY)
        t = get_city_airport_list(response.data)
        return Response({"json1": t})
    except ResponseError as error:
        return Response({"Error": error})


class Base_view(generics.GenericAPIView):
    queryset = None
    serializer_class = None
    model = None
    foreign_keys = None
    foreign_models = None
    key = None

    def get(self, request, pk):
        if pk:
            return Response(self.serializer_class(self.model.objects.filter(**{self.key: pk}), many=True).data)
        return Response(self.serializer_class(self.get_queryset(), many=True).data)

    def post(self, request, pk):
        instance = {}
        for i in request.data:
            field = i
            if i in self.foreign_keys:
                try:
                    instance[field] = self.foreign_models[field].objects.get(
                        **{self.foreign_keys[field]: request.data[field]})
                except:
                    return Response({field: f" {request.data[field]} Not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                instance[field] = request.data[i]
        new_object = self.model(**instance)
        new_object.save()
        return Response(self.serializer_class(new_object).data)

    def put(self, request, pk):
        objectp = self.model.objects.get(**{self.key: request.data[self.key]})
        instance = {}
        for i in request.data:
            field = i
            if i in self.foreign_keys:
                try:
                    instance[field] = self.foreign_models[field].objects.get(
                        **{self.foreign_keys[field]: request.data[field]})
                except:
                    return Response({field: f" {request.data[field]} Not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                instance[field] = request.data[i]
        for k, v in instance.items():
            setattr(objectp, k, v)
        objectp.save()
        return Response(self.serializer_class(objectp).data)

    def delete(self, request, pk):
        objectp = self.model.objects.get(**{self.key: request.data[self.key]})
        objectp.delete()
        return Response(self.serializer_class(objectp).data)





class Users(Base_view):
    queryset = get_user_model().objects.all()
    serializer_class = SerializerUser
    model = get_user_model()
    foreign_keys = {}
    foreign_models = {}
    key = "username"

    def post(self, request, pk):
        instance = {}
        for i in request.data:
            field = i
            if i in self.foreign_keys:
                try:
                    instance[field] = self.foreign_models[field].objects.get(
                        **{self.foreign_keys[field]: request.data[field]})
                except:
                    return Response({field: f" {request.data[field]} Not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                instance[field] = request.data[i]
        new_object = User.objects.create_user(*instance.values())
        new_object.save()
        return Response(self.serializer_class(new_object).data)

    def put(self, request, pk):
        objectp = self.model.objects.get(**{self.key: request.data[self.key]})
        instance = {}
        # print(request.data)
        for i in request.data:
            field = i
            if i in self.foreign_keys:
                try:
                    instance[field] = self.foreign_models[field].objects.get(
                        **{self.foreign_keys[field]: request.data[field]})
                except:
                    return Response({field: f" {request.data[field]} Not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if field == 'password':
                    objectp.set_password(request.data[i])
                else:
                    instance[field] = request.data[i]
        for k, v in instance.items():
            setattr(objectp, k, v)
        objectp.save()
        return Response(self.serializer_class(objectp).data)


#
class Vuelos(Base_view):
    queryset = Vuelo.objects.all()
    serializer_class = SerializerVuelo
    model = User
    foreign_keys = {'Usuario':'Correo'}
    foreign_models = {'Usuario':User}
    key = "id"
