from django.urls import path

from influencers import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('upload/', views.upload, name='upload'),
    path('top5', views.influencers_top5, name='Influencers_top5'),
    path('<int:influencer_id>/', views.influencer, name='influencer'),
]