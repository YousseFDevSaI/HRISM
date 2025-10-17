from django.urls import path
from api.views import *

urlpatterns = [
    path('excel/', Excel.as_view()),
    path('get-dim/', GetDimensions.as_view()),
    path('upload/', UploadFile.as_view()),
    path('get-files/', GetFiles.as_view()),
    path('login/', Login.as_view()),
    path('approve/', ApprovalAndLogs.as_view()),
    path('get-ca/', GetChartOfAccounts.as_view()),
]