
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 12:01:02 2021

@author: AGUS
"""

import requests
import csv
import json
from bs4 import BeautifulSoup
from datetime import datetime

#Diccionario con las variables que interesan
paises = {"yuan":"83","real":"12", "euro":"98", "peso chileno":"11", "peso uruguayo":"10", "yen": "19"}

DATE_INPUT_FORMAT = '%d/%m/%Y'
DATE_OUTPUT_FORMAT = '%d/%m/%Y'


def make_soup(url):
    with requests.get(url, stream=True) as r:
        soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse_soup(soup):
    rows = soup.find('table').find_all('tr')
    # excluyendo las primeras dos filas. Tienen metadata que no interesa
    data_rows = rows[2:]
    csv_rows = []
    for data in data_rows:
        # Parsing html and casting to python types
        row = data.find_all('td')

        date = row[0].text.lstrip('\r\n ')
        date = datetime.strptime(date, DATE_INPUT_FORMAT)

        tipo_de_cambio = row[1].text.lstrip('\r\n ').replace(',','.')
        tipo_de_cambio = float(tipo_de_cambio)

        tipo_de_cambio_2 = row[2].text.lstrip('\r\n ').replace(',','.')
        tipo_de_cambio_2 = float(tipo_de_cambio_2)

        csv_rows.append([date, tipo_de_cambio, tipo_de_cambio_2])
    return csv_rows

def output_to_file(file_name, rows):
    with open(file_name, 'w') as f:
        # aca viene la logica de como formatear en el output para que excel lo entienda
        # 
        writer = csv.writer(f)
        for row in rows:
            row[0] = row[0].strftime(DATE_OUTPUT_FORMAT)
            writer.writerow(row)
        
#Loop para bajar los archivos seleccionados
for key,value in paises.items():
    url = f"http://www.bcra.gov.ar/PublicacionesEstadisticas/Evolucion_moneda_3.asp?tipo=E&Fecha=1998.01.01&Moneda={value}"
    soup = make_soup(url)
    csv_rows = parse_soup(soup)
    # ojo que esta forma de crear los nombres va a pisar el csv anterior si lo volvemos a correr
    output_to_file(f'{key}.csv', csv_rows)
