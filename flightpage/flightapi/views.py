from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from amadeus import Client, ResponseError, Location
from rest_framework import generics
from .models import Vuelo, Hotel
from .serializer import SerializerVuelo, SerializerUser, SerializerHotel
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


# @api_view(["GET"])
# def CityHotels(request, city):
#     hoteles = []
#     offers = []
#     print('t')
#     try:
#         response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=city)
#         for i in response.data:
#             hoteles.append(i['hotelId'])
#     except ResponseError as error:
#         pass
#     for x in hoteles[0:5:]:
#         try:
#             response = amadeus.shopping.hotel_offers_search.get(hotelIds=x, adults='2')
#             if response.data:
#                 offers.append(response.data[0])
#         except ResponseError as error:
#             pass
#     print(offers)
#     return Response({'offers': offers})

@api_view(["POST"])
def CityHotels(request, city):
    print(request.data)
    hoteles = []
    offers = []
    print('t')
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=city)
        for i in response.data:
            hoteles.append(i['hotelId'])
    except ResponseError as error:
        pass
    for x in hoteles:
        try:
            response = amadeus.shopping.hotel_offers_search.get(hotelIds=x, **request.data)
            if response.data:
                offers.append(response.data[0])
        except ResponseError as error:
            pass
    print(offers)
    # offers = [{'type': 'hotel-offers', 'hotel': {'type': 'hotel', 'hotelId': 'FHGDLCC1', 'chainCode': 'FH', 'dupeId': '700070668', 'name': 'FIESTA AMERICANA GRAND GUADALAJARA COUNT', 'cityCode': 'GDL', 'latitude': 20.66622, 'longitude': -103.35181}, 'available': True, 'offers': [{'id': '9O1QWIAEY1', 'checkInDate': '2022-11-30', 'checkOutDate': '2022-12-07', 'rateCode': 'PMT', 'rateFamilyEstimated': {'code': 'PRO', 'type': 'P'}, 'room': {'type': 'A1K', 'typeEstimated': {'category': 'DELUXE_ROOM', 'beds': 1, 'bedType': 'KING'}, 'description': {'text': 'PROMOTIONAL RATE-FREE WIFI\nDELUXE KING', 'lang': 'EN'}}, 'guests': {'adults': 1}, 'price': {'currency': 'USD', 'base': '905.59', 'total': '1077.65', 'taxes': [{'code': 'TOTAL_TAX', 'amount': '172.06', 'currency': 'USD', 'included': False}], 'variations': {'average': {'base': '129.37'}, 'changes': [{'startDate': '2022-11-30', 'endDate': '2022-12-07', 'base': '129.37'}]}}, 'policies': {'guarantee': {'acceptedPayments': {'creditCards': ['AC', 'AX', 'DC', 'SD', 'DS', 'JC', 'CA', 'IK', 'MC', 'NC', 'NM', 'VA', 'VI', 'VN', 'VS'], 'methods': ['CREDIT_CARD']}}, 'paymentType': 'guarantee', 'cancellation': {'numberOfNights': 1, 'amount': '129.37', 'deadline': '2022-11-29T18:00:00-06:00'}}, 'self': 'https://test.api.amadeus.com/v3/shopping/hotel-offers/9O1QWIAEY1'}], 'self': 'https://test.api.amadeus.com/v3/shopping/hotel-offers?hotelIds=FHGDLCC1&adults=1&checkInDate=2022-11-30&checkOutDate=2022-12-07'}]
    return Response({'offers': offers})


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
                'fsalida': i['itineraries'][0]['segments'][0]['departure']['at'].partition('T')[0],
                'fllegada': i['itineraries'][0]['segments'][0]['departure']['at'].partition('T')[0],
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
        print('request.data')
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
    model = Vuelo
    foreign_keys = {'Usuario': 'username'}
    foreign_models = {'Usuario': User}
    key = "id"

class Hoteles(Base_view):
    queryset = Hotel.objects.all()
    serializer_class = SerializerHotel
    model = Hotel
    foreign_keys = {'Usuario': 'username'}
    foreign_models = {'Usuario': User}
    key = "id"


@api_view(["GET"])
def vuelosUsuario(request, user):
    queryset = Vuelo.objects.filter(Usuario__username=user)
    serializer = SerializerVuelo(queryset, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def hotelesUsuario(request, user):
    queryset = Hotel.objects.filter(Usuario__username=user)
    serializer = SerializerHotel(queryset, many=True)
    return Response(serializer.data)
