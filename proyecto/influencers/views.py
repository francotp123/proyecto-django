from django.http import HttpResponse
from django.shortcuts import render
import csv
from django.core.management.base import BaseCommand
from influencers.models import Influencers
from influencers.utils import string_to_number  # Reemplaza 'myapp' y 'MyModel' con los nombres de tu aplicación y modelo
# Create your views here.
def mainpage(request):
    return HttpResponse('Hello world!')

def upload(request):
    with open('static/top_1000_instagrammers.csv', 'r') as file:
        Influencers.objects.all().delete()
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Ignora la primera fila si contiene encabezados
        for row in reader:
            # Suponiendo que el orden de las columnas en el CSV es nombre, edad, correo
            Name, Rank, Category, Followers, Audience_Country, Authentic_Engagement, Engagement_average = row
            # convertir rank a numero
            Rank = string_to_number(Rank)
            # Convertir followers a numero
            Followers = string_to_number(Followers)
            # Convertir Authentic engagement a nummero
            Authentic_Engagement = string_to_number(Authentic_Engagement)
            #Convertir Authentic engagement a numero
            Engagement_average = string_to_number(Engagement_average)
            # Crea una nueva instancia del modelo y guárdala en la base de datos
            Influencers.objects.create(username=Name, rank=Rank, category=Category, followers=Followers, audience_country=Audience_Country, aut_eng=Authentic_Engagement, avg_eng=Engagement_average)
    return HttpResponse("OK")
