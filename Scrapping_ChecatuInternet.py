import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from lxml import html
# import re
import pandas as pd

opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option('useAutomationExtension', False)
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_argument('--disable-extensions')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-infobars')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--disable-browser-side-navigation')
opts.add_argument('--disable-gpu')  # Deshabilita la GPU

driver = webdriver.Chrome(options=opts)

url = 'https://checatuinternetmovil.osiptel.gob.pe/'

driver.execute_script(f"window.open('{url}', '_blank')")
time.sleep(random.randint(10,13))
driver.switch_to.window(driver.window_handles[1])
driver.maximize_window()

html = driver.page_source
soup = bs(html , 'html.parser') ## lxml: tipo de parseador


### captura nombres de los kpis (columnas)

kpi_1 = soup.find('span', attrs={'aria-describedby': 'cdk-describedby-message-1'}).text.strip()
kpi_2 = soup.find('span', attrs={'aria-describedby': 'cdk-describedby-message-2'}).text.strip()
kpi_3 = soup.find('span', attrs={'aria-describedby': 'cdk-describedby-message-3'}).text.strip()
kpi_4 = soup.find('span', attrs={'aria-describedby': 'cdk-describedby-message-4'}).text.strip()
kpi_5 = soup.find('span', attrs={'aria-describedby': 'cdk-describedby-message-5'}).text.strip()

mi_lista_kpis = [kpi_1, kpi_2 , kpi_3, kpi_4, kpi_5]


### captura año 

anio = 2024
mes = 'Julio'
region = 'Total'
provincia = 'Total'
distrito = 'Total'


lista_anio = []
lista_mes = []
lista_region = []
lista_provincia = []
lista_distrito = []

x=0

while x < 5:
    lista_anio.append(anio)
    lista_mes.append(mes)
    lista_region.append(region)
    lista_provincia.append(provincia)
    lista_distrito.append(distrito)
    x=x+1


################### captura de datos de los desplegables #################

# Localizar el elemento <select> por formcontrolname

meses_dropdown  = soup.find_all('select', attrs={'formcontrolname': 'mes'})  
lista_meses_dd =  []
for meses_dd in meses_dropdown:
    #print(meses_dd.text)
    lista_meses_dd.append(meses_dd.text)
    
lista_meses_dd = lista_meses_dd[0].split()
n = len(lista_meses_dd)
#print(lista_meses_dd)
# print(lista_meses_dd[0])
# print(lista_meses_dd[1])
# print(lista_meses_dd[2])

x=1
# Lista para almacenar los DataFrames
dataframes = []


while x < n:
    print(lista_meses_dd[x])
    select_element = driver.find_element(By.CSS_SELECTOR, 'select[formcontrolname="mes"]')

    # Usar Select de Selenium para interactuar con el dropdown
    select = Select(select_element)
    select.select_by_visible_text(lista_meses_dd[x])  # Selecciona la opción "Enero"
    
    time.sleep(random.randint(12,15))

    html = driver.page_source
    soup = bs(html , 'html.parser') ## lxml: tipo de parseador


    kpis_mov   = soup.find_all('td', {'class':'mat-cell cdk-cell cdk-column-movistar mat-column-movistar'})
    kpis_claro = soup.find_all('td', {'class':'mat-cell cdk-cell cdk-column-claro mat-column-claro'})
    kpis_entel = soup.find_all('td', {'class':'mat-cell cdk-cell cdk-column-entel mat-column-entel'})
    kpis_bitel = soup.find_all('td', {'class':'mat-cell cdk-cell cdk-column-bitel mat-column-bitel'})
    kpis_promedio = soup.find_all('td', {'class':'mat-cell cdk-cell cdk-column-promedio mat-column-promedio'})

    mi_lista_final = []
    datos_movistar = []
    datos_claro = []
    datos_entel = []
    datos_bitel = []
    datos_promedio = []

    ######### movistar ###########

    for velocidad_subida in kpis_mov:
        ##print(velocidad_subida.text)
        datos_movistar.append(velocidad_subida.text)

    ######### claro ###########

    for velocidad_subida in kpis_claro:
        ##print(velocidad_subida.text)
        datos_claro.append(velocidad_subida.text)

    ######### entel ###########

    for velocidad_subida in kpis_entel:
        ##print(velocidad_subida.text)
        datos_entel.append(velocidad_subida.text)

    ######### bitel ###########

    for velocidad_subida in kpis_bitel:
        ##print(velocidad_subida.text)
        datos_bitel.append(velocidad_subida.text)

    ######### promedio ###########

    for velocidad_subida in kpis_promedio:
        ##print(velocidad_subida.text)
        datos_promedio.append(velocidad_subida.text)
        
    #print(datos_movistar)   
    mi_lista_final = [mi_lista_kpis , datos_movistar, datos_claro, datos_entel, datos_bitel, datos_promedio]
    ##print(mi_lista_final)

    # El primer elemento de la lista será el nombre de las columnas
    columnas = mi_lista_final[0]

    # El segundo elemento de la lista serán los datos
    datos = mi_lista_final[1:]

    # Crear el DataFrame
    df1 = pd.DataFrame(datos, columns=columnas)

    # Lista con los nombres de las operadoras y el promedio
    operadoras = ['Movistar', 'Claro', 'Entel', 'Bitel', 'Promedio']

    #lista_meses_dd[x]

    a=0
    lista_mes = []
    while a < 5:
        
        lista_mes.append(lista_meses_dd[x])
    
        a=a+1

    # Agregar la nueva columna al DataFrame
    df1['Operadora'] = operadoras
    df1['Anio'] = lista_anio
    df1['Mes'] = lista_mes
    df1['Region'] = lista_region
    df1['Distrito'] = lista_distrito
    df1['Provincia'] = lista_provincia

    # Reordenar las columnas para que 'Operadora' esté al principio
    df1 = df1[['Operadora'] + ['Anio'] +['Mes'] +['Region'] +['Distrito'] +['Provincia'] + columnas]

    dataframes.append(df1)
    
    ##pd.set_option('display.max_columns', None)
    ##print(dataframes)
    # Mostrar el DataFrame
    
    x=x+1

# Una vez fuera del bucle, concatenar todos los DataFrames verticalmente
df_combinado = pd.concat(dataframes, ignore_index=True)


pd.set_option('display.max_columns', None)
print(df_combinado)


# colocar los datos en un csv ----------------------


df_combinado.to_csv('Scrapping_checatuinternet.csv', index = False)



#df = pd.DataFrame(mi_lista_final, columns=['kpis','Movistar'])
#print(df)


# kpi_2 = soup.find('div', {'class':'display-flex-center p-r-25'}).find('span',{'class':'mat-tooltip-trigger'}).text.strip()
# kpi_3 = soup.find('div', {'class':'display-flex-center p-r-25'}).find('span',{'class':'mat-tooltip-trigger'}).text.strip()
# kpi_4 = soup.find('div', {'class':'display-flex-center p-r-25'}).find('span',{'class':'mat-tooltip-trigger'}).text.strip()

# print(kpi_1 +' '+ velocidad_subida_4g_mov)
# print(kpi_1 +' '+ velocidad_subida_4g_claro)
# print(kpi_1 +' '+ velocidad_subida_4g_entel)
# print(kpi_1 +' '+ velocidad_subida_4g_bitel)
# print(kpi_1 +' '+ velocidad_subida_4g_prom)


