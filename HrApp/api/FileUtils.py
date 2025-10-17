import math
from django.conf import settings
from .models import *
import pandas as pd
import os
from datetime import datetime


class File_Utils:
    
    def __init__(self, data) -> None:
        self.data = data

    def add_file(self):
            
            data = self.data
            file_name = data["name"]
            file_date = datetime.now().date()
            
            file = File(name = file_name,
                        date_uploaded_in = file_date)
            file.save()

    def get_excel_file_names(self):
        """
        Reads Excel file names from the specified directory and returns them in a list.

        :return: A list of Excel file names.
        """
        document_root = settings.MEDIA_ROOT
        excel_files_dir = document_root

        # Get list of all files in the directory
        all_files = os.listdir(excel_files_dir)

        # Filter the list to include only Excel files
        excel_files = [f for f in all_files if f.endswith('.xlsx') or f.endswith('.xls')]

        return excel_files
    
    def read_excel_full(self):
        """
        Reads headers and rows from an Excel sheet and maps them together.

        :return: A list of dictionaries with headers as keys and lists of cell values as values, including an 'id' key.
        """
        file_name = f"{self.data['excelSheetName']}"
        document_root = settings.MEDIA_ROOT
        file_path = os.path.join(document_root, file_name)

        # Read the Excel file
        df = pd.read_excel(file_path, header=0)
        
        # Get the header names
        headers = df.columns.tolist()
        
        # Add an 'id' header
        headers.insert(0, 'id')
        
        # Convert the DataFrame to a list of lists
        rows = df.values.tolist()
        
        # Map headers to rows with an additional 'id' field
        full_data = [{'id': idx + 1, **dict(zip(headers[1:], row))} for idx, row in enumerate(rows)]
        
        return self.clean_nan_values(full_data)
    
    
    def clean_nan_values(self, data):
        cleaned_data = data.copy()
        
        def convert_nan_to_null(value):
            if isinstance(value, float) and math.isnan(value):
                return None
            elif isinstance(value, dict):
                return {k: convert_nan_to_null(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [convert_nan_to_null(item) for item in value]
            else:
                return value
        
        return convert_nan_to_null(cleaned_data)
    
    def user_login(self):
        
        email_input = self.data['Email']
        
        if User.objects.filter(email = email_input).exists():
            return 'User Exist'
        else:
            return "User doesn't exist"
        
        
    def get_user_role(self):
        
        email_input = self.data['Email']

        return  User.objects.get(email = email_input).department
    
    def approveFile(self):
        
        email_input = self.data["userEmail"]
        file_input = self.data["excelSheetName"]
        
        file_query = File.objects.get(name = file_input)
        user = User.objects.get(email = email_input)
        approval_list = eval(file_query.approved_by)
        if user.department in approval_list:
            pass
        else:
            approval_list.append(user.department)
            file_query.approved_by = (approval_list)
            new_log = Log(
                action = f"Approved by {user.name} from {user.department}",
                file_name = file_query.name
            )
            file_query.save()
            new_log.save()
            
    def get_approvals(self):
        
        file_input = self.data["excelSheetName"]
        
        log_query = Log.objects.filter(file_name = file_input).values_list()
        
        actions = []
        for action in log_query:
            actions.append(action[1])
        return actions
