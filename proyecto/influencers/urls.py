from django.urls import path

from influencers import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('upload/', views.upload, name='upload'),
    path('influencers/', views.influencers_main, name='Influencers_main'),
    path('<int:influencer_id>/', views.influencer, name='influencer'),



]