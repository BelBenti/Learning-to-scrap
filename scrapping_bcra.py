# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 12:01:02 2021

@author: Belen
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import requests
import csv
import json

#Diccionario con las variables que interesan
paises = {"yuan":"83","real":"12", "euro":"98", "peso chileno":"11", "peso uruguayo":"10", "yen": "19"}

#Hago una función para descargar archivos
def download_file(url,key):
    local_filename = f"{key}.xls"
    #local_filename = url.split('/')[-1]
    #local_filename = local_filename + ".xlsx"
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

#Loop para bajar los archivos seleccionados
for key,value in paises.items():
    url = f"http://www.bcra.gov.ar/PublicacionesEstadisticas/Evolucion_moneda_3.asp?tipo=E&Fecha=1998.01.01&Moneda={value}"
    download_file(url,key)
# la f formatea el string de una manera particular: todo lo que vaya entre corchetes va a ser reemplazada
    