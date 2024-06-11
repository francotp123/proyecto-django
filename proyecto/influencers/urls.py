from django.urls import path

from influencers import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.mainpage, name='mainpage'), #Página principal
    path('upload/', views.upload, name='upload'), #Sube el dataset al model
    path('Influencers_top5/', views.influencers_top5, name='Influencers_top5'), #Ranking y estadísticas 
    path('top10_avg/', views.influencers_top10_avg, name='top10_avg'), #Top 10
    path('tabla/', views.tabla, name='tabla'), #Tabla
    path('unificar_cat/', views.unificar_categorias_similares, name='unificar_cat'), #Cuando se ejecuta unifica categorías
    path('prediccion/', views.prediccion, name="prediccion")  #Predicción
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 