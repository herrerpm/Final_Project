from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='GoJxdZIivaehEX52UiZVUlGS7Ob0sm6H',
    client_secret='tFOeUaHd2sKASvqd'
)

def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode']+', '+data[i]['name'])
    result = list(dict.fromkeys(result))
    return result

# Create your views here.
@api_view(["GET"])
def Prueba(request):
    return Response({"dd":"d"})

@api_view(["POST"])
def Prueba(request):
    print(request.data['json1'])
    return Response({"si":"d"})

@api_view(["POST"])
def airportcode(request):
    try:
        response = amadeus.reference_data.locations.get(keyword=request.data.get("code", " "), subType=Location.ANY)
        t = get_city_airport_list(response.data)
        print(t)
        return Response({"json1": t})
    except ResponseError as error:
        return Response({"Error":error})

