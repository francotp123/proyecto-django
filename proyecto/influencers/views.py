from django.http import HttpResponse
from django.shortcuts import render
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from influencers.utils import string_to_number
from influencers.models import Influencers
from io import BytesIO
import base64  
# Create your views here.
def mainpage(request):
    return HttpResponse('Hello world!')

def upload(request, influencer_id):
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
def influencers_top5(request):
    # Recupera los primeros 5 elementos del modelo según un atributo específico
    datos = Influencers.objects.order_by('-followers')[1:6]
    # Extrae los valores de los atributos para el gráfico de barras
    etiquetas = [obj.username for obj in datos]
    valores1 = [obj.followers for obj in datos]
    print (valores1)
    # Crea el gráfico de barras
    plt.figure(figsize=(10, 6))

    plt.bar(etiquetas, valores1, color='blue', label='Atributo 1')
    
    plt.xlabel('Influencers')
    plt.ylabel('Seguidores')
    plt.title('Gráfico de Barras - Top 5')
        # Formatear las etiquetas del eje y para mostrar los números completos
    def y_formatter(x, pos):
        return f'{int(x):,}'.replace(',', ' ')

    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))

    # Guarda el gráfico en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    # Pasa la imagen codificada a la plantilla
    return render(request, 'influencers_top5.html', {'image_base64': image_base64})


def influencer(request, influencer_id):
    return HttpResponse(f'Este es el influencer N° {influencer_id}')
    
def influencers_top10_avg(request):
    datos = Influencers.objects.order_by('-avg_eng')[:10]

    # Extrae los valores de los atributos para el gráfico de barras
    etiquetas_ = [obj.username for obj in datos]
    valores1_ = [obj.avg_eng for obj in datos]

    # Crea el gráfico de barras
    plt.figure(figsize=(10, 6))

    plt.bar(etiquetas_, valores1_, color='blue')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.4)

    plt.xlabel('Influencers')
    plt.ylabel('Engagement Avg')
    plt.title('Top 10 Influencers con mayor Engagement Avg')
        # Formatear las etiquetas del eje y para mostrar los números completos
    def y_formatter(x, pos):
        return f'{int(x):,}'.replace(',', ' ')

    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))

    # Guarda el gráfico en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    # Pasa la imagen codificada a la plantilla
    return render(request, 'influencers_top10_eng.html', {'image_base64': image_base64})