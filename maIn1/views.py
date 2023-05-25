from django.shortcuts import render
import pandas as pd
import sqlite3
import urllib.request
from django.db import connection
from django.http import JsonResponse
from django.views import View


class LoadDataView(View):
    def get(self, request):
        
        url = "https://ohiodnr.gov/static/documents/oil-gas/production/20210309_2020_1%20-%204.xls"
        filename = r"C:\Users\hp\Downloads\excelsheets.xls"
        excelsheets = filename
        urllib.request.urlretrieve(url, excelsheets)

        
        data = pd.read_excel(excelsheets)

      
        annual_data = data.groupby("API WELL  NUMBER").sum().reset_index()

        annual_data_json = annual_data.to_json(orient='records')

        with connection.cursor() as cursor:
           
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS annual_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Type TEXT,
                    Year INTEGER
                )
            """)

            
            cursor.execute("DELETE FROM annual_data")

            
            for _, row in annual_data.iterrows():
                cursor.execute("INSERT INTO annual_data (Type, Year) VALUES (%s, %s)",
                               [row['Type'], row['Year']])

            
            cursor.execute("SELECT COUNT(*) FROM annual_data WHERE Type = 'Oil'")
            oil_count = cursor.fetchone()[0]  # Fetch the oil count value from the result

            cursor.execute("SELECT COUNT(*) FROM annual_data WHERE Type = 'Gas'")
            gas_count = cursor.fetchone()[0]  # Fetch the gas count value from the result

            cursor.execute("SELECT COUNT(*) FROM annual_data WHERE Type = 'Brine'")
            brine_count = cursor.fetchone()[0]  # Fetch the brine count value from the result

            
            response_data = {
                'Oil': oil_count,
                'Gas': gas_count,
                'Brine': brine_count
            }
            return JsonResponse(response_data)


class AnnualDataView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM annual_data")
            results = cursor.fetchall()

        return render(request, 'my_template.html', {'results': results})
