from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
@api_view(["GET"])
def Prueba(request):
    return Response({"dd":"d"})

@api_view(["POST"])
def Prueba(request):
    print(request.data)
    return Response({"Mami que flow":"d"})