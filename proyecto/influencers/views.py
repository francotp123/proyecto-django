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
from django.core.paginator import Paginator
import numpy as np
import pandas as pd
import seaborn as sns
# Create your views here.

#html main
def mainpage(request):
    return render(request, 'mainpage.html')

#Subir el dataset al modelo convirtiendo los datos con la función.
def upload(request):
    with open('staticfiles/top_1000_instagrammers.csv', 'r') as file:
        Influencers.objects.all().delete()
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Ignora la primera fila si contiene encabezados
        for row in reader:
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
    
    followers = list(Influencers.objects.values_list('followers', flat=True)) #Crea una lista con la cantidad de seguidores.
    
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

    statistics = {        #Diccionario con los datos estadísticos 
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

#View para la tabla
def tabla(request):
    influencers_list = Influencers.objects.all()
    paginator = Paginator(influencers_list, 50)  # Mostrar 50 influencers por página

    page_number = request.GET.get('page')
    influencers = paginator.get_page(page_number)

    context = {
        "influencers": influencers
    }
    return render(request, 'tabla2.html', context)

#View para el top 10
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
    
    influencers = Influencers.objects.all()
    followers = [influencer.followers for influencer in influencers]
    avg_eng = [influencer.avg_eng for influencer in influencers]
    correlation = np.corrcoef(followers, avg_eng)[0, 1]

    # Crear una figura de matplotlib para el heatmap
    plt.figure(figsize=(8, 6))
    sns.set(style="whitegrid")  # Estilo del heatmap
    data = np.corrcoef(followers, avg_eng)
    sns.heatmap(data, annot=True, cmap='coolwarm', square=True,
                xticklabels=['Followers', 'Avg Engagement'], yticklabels=['Followers', 'Avg Engagement'],
                cbar_kws={'shrink': 0.7})
    plt.title('Matriz de Correlación entre Followers y Avg Engagement')
    plt.xlabel('Features')
    plt.ylabel('Features')

    # Guardar el gráfico en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'image_base64': image_base64,
        'correlation_matrix': image_base,
    }

    # Renderizar la plantilla 'top10_eng.html' con los datos
    return render(request, 'top10_eng.html', context)


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
            similar_categories = [cat for cat in categories if Levenshtein.distance(category.lower(), cat.lower()) < 25]
            
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


#View predicción
def prediccion(request):
    influencer = None # Inicializa la variable influencer con None
    if request.method == 'POST': # Verifica si la solicitud es de tipo POST
        form = CategoryForm(request.POST) # Crea una instancia del formulario con los datos POST
        if form.is_valid(): # Verifica si los datos del formulario son válidos
            # Extrae los datos limpios del formulario
            category = form.cleaned_data['category']
            company_size = form.cleaned_data['company_size']
            audience_country = form.cleaned_data['audience_country']

            # Filtra los influencers según la categoría y el país de la audiencia, y los ordena por seguidores en orden descendente
            influencers = Influencers.objects.filter(category=category, audience_country=audience_country).order_by('-followers')

            # Selecciona un influencer basado en el tamaño de la empresa
            if company_size == 'large' and influencers: # Si la empresa es grande y hay influencers
                influencer = influencers.first()  # Selecciona el influencer con más seguidores
            elif company_size == 'small' and influencers: # Si la empresa es pequeña y hay influencers
                influencer = influencers.last() # Selecciona el influencer con menos seguidores
            elif company_size == 'medium' and influencers: # Si la empresa es mediana y hay influencers
                middle_index = len(influencers) // 2 # Calcula el índice medio
                influencer = influencers[middle_index] # Selecciona el influencer en la posición media

    else:
        form = CategoryForm() # Si la solicitud no es POST, crea una instancia vacía del formulario

    # Renderiza la plantilla 'prediction.html' con el formulario y el influencer seleccionado (si hay alguno)
    return render(request, 'prediction.html', {'form': form, 'influencer': influencer})