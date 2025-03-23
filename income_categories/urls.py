from django.urls import path
from .views import IncomeCategoryListCreateView, IncomeCategoryRetrieveUpdateDestroyView

urlpatterns = [
    path('', IncomeCategoryListCreateView.as_view(), name='income-category-list-create'),
    path('<int:pk>/', IncomeCategoryRetrieveUpdateDestroyView.as_view(), name='income-category-retrieve-update-destroy'),
]