from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.core.serializers import serialize
from datetime import datetime
from .models import *
from .FileUtils import File_Utils as FU
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .msal import *

# Create your views here.
class Excel(APIView):
    def post(self, request, *args, **kwargs):
        
        try:
        
            data = json.dumps(request.data)
            dici = json.loads(data)
            
            rows = FU(dici).read_excel_full()
            return JsonResponse({"lines" : rows}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        
        try:
        
            
            excelfiles = FU({}).get_excel_file_names()
            
            return JsonResponse({"Excel Files" : excelfiles}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
        
class UploadFile(APIView):
    
        def post(self, request, *args, **kwargs):
            try:
                # Extract the file and other data from the request
                file = request.FILES['file']
                file_name = request.POST.get('file_name', file.name)

                # Save the file to the storage
                file_path = default_storage.save(file_name, ContentFile(file.read()))

                # Prepare data to be passed to the add_file method
                data = {
                    'name': file_name
                }
                
                FU(data).add_file()
                return JsonResponse({'message': 'Added'}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)

class GetDimensions(APIView):
    
    def get(self, request, *args, **kwargs):
        
        try:
            
            dim = []
            query = Dimesnsion.objects.all().values()
            for line in query:
                details = {'column' : line['attribute_name'], 'row' : line['row_attribute']}
                dim.append(details)
            return JsonResponse({"dimesnsion" : dim}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
        
class GetFiles(APIView):
    
    def get(self, request, *args, **kwargs):
        
        try:
            files_query = File.objects.all().values()
            file_names = []
            for file in files_query:
                file_names.append(file['name'])
                
            return JsonResponse({"Files" : file_names}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.dumps(request.data)
            dici = json.loads(data)
            
            stat = {"Status" : FU(dici).user_login()}
            
            return JsonResponse(stat, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        try:
            data = json.dumps(request.data)
            dici = json.loads(data)
            
            department = {"Department" : FU(dici).get_user_role()}
            
            return JsonResponse(department, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
        
class ApprovalAndLogs(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.dumps(request.data)
            dici = json.loads(data)
            
            FU(dici).approveFile()
            
            return JsonResponse("Approved", status=status.HTTP_200_OK, safe=False)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        try:
            data = json.dumps(request.data)
            dici = json.loads(data)
            
            actions = {"actions":FU(dici).get_approvals()}
            
            return JsonResponse(actions, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)

class GetChartOfAccounts(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            return JsonResponse({"Accounts":get_chart_of_accounts()}, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
                return Response(f"Request Failed Due to {e}", status=status.HTTP_400_BAD_REQUEST)
            
            
            
            
            
            
            
            
            
            
            
            