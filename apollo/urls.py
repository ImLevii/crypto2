"""
apollo URL Configuration
https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""
from django.urls import path
from django.contrib import admin

from apollo.api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # crypto exchange
    path('api/store/ipn', views.IPNCallbackView.as_view()),
    path('api/store/vars', views.GetStoreVariablesView.as_view()),
    path('api/store/exchange-rate', views.GetExchangeRateView.as_view()),
    path('api/store/tx/create', views.CreateTransactionView.as_view()),
    path('api/store/tx/info', views.TransactionInfoView.as_view()),
]
