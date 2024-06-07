from django.urls import path

from influencers import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('upload/', views.upload, name='upload'),
    path('Influencers_top5/', views.influencers_top5, name='Influencers_top5'),
    path('<int:influencer_id>/', views.influencer, name='influencer'),
    path('top10_avg/', views.influencers_top10_avg, name='top10_avg'),
    path('tabla/', views.tabla, name='tabla'),
    path('unificar_cat/', views.unificar_categorias_similares, name='unificar_cat')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)