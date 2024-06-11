import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from influencers.utils import string_to_number
from influencers.models import Influencers
from io import BytesIO
import base64  
from influencers.forms import CategoryForm
import math
# Create your views here.
def mainpage(request):
    return render(request, 'mainpage.html')

def upload(request):
    with open('staticfiles/top_1000_instagrammers.csv', 'r') as file:
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
    datos = Influencers.objects.order_by('-followers')[:5]
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
    
    followers = list(Influencers.objects.values_list('followers', flat=True))
    
    if not followers:
        return render(request, 'stats/statistics.html', {'error': 'No data available'})

    # Calcula estadísticos básicos
    count = len(followers)
    mean = sum(followers) / count
    min_value = min(followers)
    max_value = max(followers)
    sorted_data = sorted(followers)
    
    # Calcula la mediana
    if count % 2 == 0:
        median = (sorted_data[count // 2 - 1] + sorted_data[count // 2]) / 2
    else:
        median = sorted_data[count // 2]

    statistics = {
        'count': count,
        'mean': mean,
        'min': min_value,
        'max': max_value,
        'median': median,
    }
    # Pasa la imagen codificada a la plantilla
    context = {
        'image_base64': image_base64,
        'statistics' : statistics

    }
    return render(request, 'firstgraph.html', context)


def influencer(request, influencer_id):
    return HttpResponse(f'Este es el influencer N° {influencer_id}')
def tabla(request):
    influencers = Influencers.objects.all()
    context = {
        "influencers":influencers
    }
    return render(request, 'tabla2.html', context)
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
    return render(request, 'top10_eng.html', {'image_base64': image_base64})


import Levenshtein

def unificar_categorias_similares(request):
    # Obtener todas las categorías únicas en la base de datos excluyendo las vacías
    categories = Influencers.objects.exclude(category__isnull=True).exclude(category__exact='').values_list('category', flat=True).distinct()
    
    print("hola", categories)

    # Inicializar un diccionario para almacenar las categorías unificadas
    categories_unified = {}
    
    # Unificar categorías basadas en similitudes
    for category in categories:
        # Comprobar si la categoría ya ha sido unificada
        if category not in categories_unified:
            # Buscar categorías similares
            similar_categories = [cat for cat in categories if Levenshtein.distance(category.lower(), cat.lower()) < 15]
            
            # Unificar todas las categorías similares a la primera categoría encontrada
            for similar in similar_categories:
                categories_unified[similar] = category
    
    print(categories_unified)

    # Actualizar las categorías en la base de datos
    for obj in Influencers.objects.all():
        if obj.category in categories_unified:
            obj.category = categories_unified[obj.category]
            obj.save()
    
    return JsonResponse({'status': 'Categorías unificadas con éxito'})
"""
def prediccion(request):
    top_instagrammer = None

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            top_instagrammer = Influencers.objects.filter(category=category).order_by('-followers').first()
    else:
        form = CategoryForm()
    
    return render(request, 'prediction.html', {'form': form, 'top_instagrammer': top_instagrammer})
"""
def prediccion(request):
    influencer = None
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            company_size = form.cleaned_data['company_size']
            audience_country = form.cleaned_data['audience_country']

            influencers = Influencers.objects.filter(category=category, audience_country=audience_country).order_by('-followers')

            if company_size == 'large' and influencers:
                influencer = influencers.first()
            elif company_size == 'small' and influencers:
                influencer = influencers.last()
            elif company_size == 'medium' and influencers:
                middle_index = len(influencers) // 2
                influencer = influencers[middle_index]

    else:
        form = CategoryForm()

    return render(request, 'prediction.html', {'form': form, 'influencer': influencer})