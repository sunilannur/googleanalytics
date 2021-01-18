from django.urls import path
from . import views

app_name = "googleanalytics"
urlpatterns = [

    path('google/', views.google_test, name="google_test"),
    path('', views.tracker, name="tracker"),

]
