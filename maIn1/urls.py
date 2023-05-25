from django.urls import path

from .views import LoadDataView

urlpatterns = [
    path('', LoadDataView.as_view(), name='load_data'),
    path('annual-data/', AnnualDataView.as_view(), name='annual-data'),
]
