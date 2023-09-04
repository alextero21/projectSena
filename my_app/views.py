from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from asgiref.sync import async_to_sync
import json
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import NoSuchElementException
from django.core.files.storage import default_storage
import os
import re
from django.conf import settings
from selenium.common.exceptions import TimeoutException
from difflib import get_close_matches


global_driver = None
url = 'https://sena.territorio.la/'
url_perfil_id = 'perfil.php?id=31247202'
# Ruta al controlador ChromeDriver
# chrome_driver_path = 'C:\dchrome\chromedriver.exe'  # (o .exe en Windows)



import time

def findSubjectsByTeacher(teacher_name):
        profesor_materia = {
        "MARIA ELENA MONTUFAR MUÑOZ": "ASESORAR CONSUMIDOR FINANCIERO",
        "ALEX FERNANDO LOPEZ": "AMBIENTAL Y SST",
        "JAIME MAURICIO CRUZ": "UTILIZAR HERRAMIENTAS OFIMATICAS",
        "NAZLY YULIANA BENJUMEA BECERRA": "INGLÉS",
        "DANIEL DOMINGUEZ CABAL": "ÉTICA",
        "ISABEL VALENCIA PUENTES": "COMUNICACIONES",
        "YULIETH JARAMILLO OSPINA": "RAZONAMIENTO CUANTITATIVO",
        "EDGAR DE JESUS ARENAS VARGAS": "MANEJAR RECURSOS FINANCIEROS",
        "JORGE ELIECER VERA TASAMA": "DERECHOS FUNDAMENTALES",
        "HERMINSUL VALLES ESPINOSA": "CULTURA FÍSICA",
        }

        # nombre_profesor_buscado = "MARIA LENA MONTUFAR"

        # Buscar la coincidencia más cercana usando la función get_close_matches
        matches = get_close_matches(teacher_name.upper(), profesor_materia.keys(), n=1, cutoff=0.6)

        if matches:
            profesor_mas_similar = matches[0]
            materia_correspondiente = profesor_materia[profesor_mas_similar]
            # print(f"¿Quisiste decir '{profesor_mas_similar}'?")
            # print(f"La materia es: {materia_correspondiente}")
        else:
            # print(f"No se encontró un profesor similar a '{teacher_name}'")
            materia_correspondiente= False
            
        return materia_correspondiente


def initialize_driver():
    # Ruta al ejecutable del controlador Chrome
    driver_path = 'C:\dchrome\chromedriver.exe'

    # Configurar opciones del controlador Chrome
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Ejecución en segundo plano

    # Crear instancia del servicio del controlador
    service = Service(executable_path=driver_path)

    # Crear instancia del controlador Chrome
    return webdriver.Chrome(service=service, options=chrome_options)

def login(request):#La pagina mia

    return render(request, 'login.html')

def is_driver_active(driver):
    try:
        # Verificar si el controlador tiene una instancia válida
        if driver and driver.title:
            # Verificar si el navegador tiene una ventana abierta
            return True
    except WebDriverException:
        pass
    return False

@csrf_protect
def activateDriver(request):#ESTE NOOOOO
    global global_driver
    
   
    # Comprobar si el controlador está activo
    # if global_driver and is_driver_active(global_driver):

    if global_driver and is_driver_active(global_driver):
        # Continuar interactuando con el navegador ya abierto

        if request.method == 'POST':     
            user = int(request.POST.get('username'))
            password = request.POST.get('password')

            if user == 1234192477 and password == 'Colgate123456':    
                
                global_driver.get(url + 'index.php?login=true')
                wait = WebDriverWait(global_driver, 10)

                usuario = wait.until(EC.presence_of_element_located((By.ID, "document")))
                contrasena = wait.until(EC.presence_of_element_located((By.ID, "passwd")))
                usuario.send_keys(user)
                contrasena.send_keys(password)

                contrasena.send_keys(Keys.ENTER)              

                

           
                return JsonResponse({'status':200, 'message':'Éxito','url':'home'})

                
            else:

                return JsonResponse({'status':404, 'message':'No coincide el usuario o constraseña'})
            

    else:
        # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
        global_driver = initialize_driver()
        global_driver.get(url + 'index.php?login=true')
    
        return JsonResponse({'status':200, 'message':'Abriendo controlador'})

@csrf_protect            
def find_post(request):

    global global_driver
    
    if global_driver and is_driver_active(global_driver):

        if request.POST.get('tarea_id'):

            tarea_id=request.POST.get('tarea_id')
            print('tarea_id',tarea_id)

            # AQUI COMIENZA EL PERFIL
            
            # Se da clic en evidencias
            # http://sena.territorio.la/tarea_tt.php?tarea=479413805

            
            global_driver.get(url+'tarea_tt.php?tarea='+str(tarea_id))
    
            if request.POST.get('vinculo') or request.FILES.getlist('files[]'):#Estos REQUEST son obtenidos de mi pagina interfaz

                if request.FILES.getlist('files[]'):
                    archivos = request.FILES.getlist('files[]')

                    wait = WebDriverWait(global_driver, 10)

                    # Encuentra el elemento de entrada de archivo (input type="file") por su atributo "name" o "id"
   
                    archivo_ruta = []  # Inicializa la lista para las rutas de los archivos

                    for archivo in archivos:
                        # Aquí puedes acceder a los datos del archivo, por ejemplo:
            
                        # Guarda el archivo en el sistema de archivos (por ejemplo, en el directorio "uploads")
                        archivo_path = default_storage.save(f"{archivo.name}", archivo)
                        
                        # Convierte la ruta relativa a absoluta
                        archivo_path_abs = os.path.abspath("uploads/"+archivo_path)

                        archivo_ruta.append(archivo_path_abs)

                    
                    input_archivo = wait.until(EC.presence_of_element_located((By.ID, "file")))

                    # Agrega la ruta del archivo a la lista
                    input_archivo.send_keys("\n".join(archivo_ruta))
                    

                #Si se ha typeado un vinculo, entonces se activa el find_element
                if request.POST.get('vinculo'):
                    text_vinculo = request.POST.get('vinculo')
                    contentSena= global_driver.find_element(By.XPATH, '//*[@id="divVinculosRespuesta"]/a')
                    contentSena.click()
                    input_vinculo = global_driver.find_element(By.ID, "linktare")
                    input_vinculo.send_keys(text_vinculo)    
                
                # Cuando esté todo ok, se procede a activar el boton de abajo!
                # boton_enviar = global_driver.find_element(By.XPATH, "//*[@id='contestarTareaBoton']")
                # boton_enviar.click()




            
            return JsonResponse({'status':200, 'data':tarea_id})
        
        else:
            return JsonResponse({'status': 400, 'message': 'ERROR2'})

    else:
        # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
        # global_driver = initialize_driver()
        # global_driver.get(url + 'index.php?login=true')

        return JsonResponse({'status': 400, 'message': 'ERROR DEL BUENO'})
  
def home(request):


    global global_driver

    if global_driver and is_driver_active(global_driver):

        # if request.POST.get('pagina'):
        wait = WebDriverWait(global_driver, 10)
        contentSena= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="catalogo-main-content"]')))
        contenido_html = contentSena.get_attribute('innerHTML')
        soup = BeautifulSoup(contenido_html, 'html.parser')
        elementos_con_clase = soup.find_all(lambda tag: tag.has_attr('class') and 'letras1' in tag['class'])
        contenido_class = [{'url':url,'texto': elemento.get_text(), 'href': elemento.get('href').replace('?', '%3F').replace('=', '%3D')} for elemento in elementos_con_clase]

        

        
        return render(request, 'home.html',{'content':contenido_class})

    
    else:
            # Código para manejar el inicio de sesión fallido
        # return render(request, 'upload.html')
        # return JsonResponse({'status':200, 'message':'Excelente','url':'test'})
        # global_driver = initialize_driver()
        # global_driver.get(url + 'index.php?login=true')

        return render(request, 'home.html',{'content':'123'})

    # return HttpResponseRedirect('/login')

def get_url(request,href):

    if global_driver and is_driver_active(global_driver):
        
        global_driver.get(url+href)

        return JsonResponse({'status':200, 'message':'Excelente','url':'test'})
    else:
      return JsonResponse({'status':404, 'message':'Error en el navegador','url':'home'})

@csrf_protect
def test(request):

    id_clase='2776992'

    global global_driver

    if global_driver and is_driver_active(global_driver):


        if request.POST.getlist('id_tareas'):
            listNumber = request.POST.getlist('id_tareas')  # Obtener el valor como lista
            indexTarea = int(listNumber[0]) if listNumber else None  # Obtener el primer elemento de la lista y convertirlo a entero
            if(isinstance(indexTarea,int)):
                time.sleep(1) 

                global_driver.get(url+'tarea_tt.php?tarea='+str(indexTarea))
            
                wait = WebDriverWait(global_driver, 10)
                divInformacionTarea = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="divInformacionTarea"]')))#//*[@id="FechaTareaInicio"]
                
                # Obtener el valor de FechaTareaInicio
                # fecha_tarea_inicio = divInformacionTarea.find_element(By.XPATH, '//span[@id="FechaTareaInicio"]').text
                
                # Obtener el valor de FechaTarea
                fecha_tarea = divInformacionTarea.find_element(By.XPATH, '//span[@id="FechaTarea"]').text
                nombre_profesor = divInformacionTarea.find_element(By.XPATH, '//*[@id="divInformacionTarea"]/table/tbody/tr/td[2]/span[5]/strong').text

                # Obtener el texto de ConTare
                ConTituloBtc = divInformacionTarea.find_element(By.ID, 'ConTituloBtc').text
                con_tare_texto = divInformacionTarea.find_element(By.ID, 'ConTare').text

                try:

                    if divInformacionTarea.find_element(By.XPATH, '//*[@id="post_load"]').text != "":
                        hay_tareas=True
                    else:
                        hay_tareas=False
                    
                except:
                    hay_tareas=False

                evidence = [
                    {
                        "id_classroom": id_clase,
                        "classroom": "Técnico en Servicios Comerciales y Financieros",
                        "status": 200,
                        "materia": findSubjectsByTeacher(nombre_profesor),
                        "id_tarea": indexTarea,
                        "didHomework": str(hay_tareas),
                        "date_end": fecha_tarea,
                        "names": nombre_profesor,
                        "content": ConTituloBtc+': '+con_tare_texto
                    
                    }
                ]
                
            
            return JsonResponse({'data_evidence': evidence})  
         
        else:

            if request.POST.get('id_career'):#Aqui se traen todos los numeros POST o numeros de evidencias del respectivo curso o carrera

                listCareer = request.POST.get('id_career')  # Obtener el valor como lista
                indexCareer = str(listCareer) if listCareer else None  # Obtener el primer elemento de la lista y convertirlo a entero
                if(isinstance(indexCareer,str)):
                    
                    global_driver.get(url+'tareas.php?clase='+indexCareer)
                    
                    # Esperar a que el elemento esté presente en la página
                    wait = WebDriverWait(global_driver, 10)
                    div_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divContentListaTareas"]/div[starts-with(@id, "tarea")]')))

                    # Lista para almacenar los números de tarea
                    numeros_tarea = []

                    # Iterar a través de los elementos div
                    for div_element in div_elements:
                        numero_tarea = div_element.get_attribute("id").replace("tarea[", "").replace("]", "")
                        numeros_tarea.append(numero_tarea)

                # return JsonResponse({'numeros_tarea':len(numeros_tarea),'id_tareas': numeros_tarea})   
                jsonResponse={'id_career':indexCareer,'id_tareas': numeros_tarea,'status':200}
                

            elif request.POST.getlist('career'):#Aqui se obtienen todos los cursos o carreras

                global_driver.get(url+'init.php')

                # Encuentra todos los elementos <a> que tienen un atributo href
                enlaces = global_driver.find_elements(By.CSS_SELECTOR,('a[href*="detalle_curso.php"]'))

                id_career=[]
                title=[]
                # for enlace in enlaces:
                for enlace in enlaces:
                    # Itera a través de los enlaces y obtén el valor del atributo href
                    href = enlace.get_attribute("href")
                    id_value = href.split("=")[-1]
                    title_valor = enlace.get_attribute("title")

                    # Comprueba si los valores de "id" y "title" no están vacíos
                    if id_value and title_valor:
                        # Ahora puedes procesar los valores de "id" y "title", por ejemplo, imprimirlos
                        id_career.append(id_value)
                        title.append(title_valor)
                    

                jsonResponse={'id_career': id_career,'title':title,'status':200}
            
            else:#Si no hay datos enviados
                jsonResponse={'status':400}

            return JsonResponse(jsonResponse)

    else:
            # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
            global_driver = initialize_driver()
            global_driver.get(url + 'index.php?login=true')
            numeros_tarea=0
            primer_elemento=0
            
            return JsonResponse({'numeros_tarea':numeros_tarea,'primer': primer_elemento})

    #https://sena.territorio.la/tareas.php?clase=2776992

    #1234192477
    #Colgate123456


def getContent(request):

    global global_driver

    if global_driver and is_driver_active(global_driver):
            
        # AQUI COMIENZA EL MURO

        global_driver.get(url+'init.php?muro=1')
        # global_driver.get('http://localhost:8000/probar')
        #https://sena.territorio.la/tareas.php?clase=2776992

  
        unique_posts = []

        element_tarea = []
        element_name = []
        previous_num_elements = 0
        contenidoEvidencias=[]
        element_fechaEntrega=[]

        while True:
            try:
                ver_mas_button = WebDriverWait(global_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Ver más')]"))
                )
                ver_mas_button.click()
                time.sleep(1) 

                WebDriverWait(global_driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'post')]"))
                )
                
                current_num_elements = len(global_driver.find_elements(By.XPATH, "//div[starts-with(@id, 'post')]"))
                if current_num_elements == previous_num_elements:
                    break
                previous_num_elements = current_num_elements
            except NoSuchElementException:
                break

        # Capturar todos los "post" después de cargar todos los datos
        post_elements = global_driver.find_elements(By.XPATH, "//div[starts-with(@id, 'post')]")
        for post_element in post_elements:
            nombres_elements = post_element.find_elements(By.CLASS_NAME, "nombres")
            for nombres_element in nombres_elements:
                href = nombres_element.get_attribute("href")
                parsed_url = urlparse(href)
                grupo_param = parse_qs(parsed_url.query).get("grupo")
                if grupo_param and grupo_param[0] == "2776992":
                    boton_elements = post_element.find_elements(By.CLASS_NAME, "botonPersonalizadoBootstrap")
                    for boton_element in boton_elements:
                        href_boton = boton_element.get_attribute("href")
                        parsed_url_boton = urlparse(href_boton)
                        tarea_param = parse_qs(parsed_url_boton.query).get("tarea")
                        if tarea_param:
              
                            # Buscar otros elementos dentro de post_element
                            element_name.append(post_element.find_element(By.CLASS_NAME, "nombres").text)
                            element_fechaEntrega.append(post_element.find_element(By.CLASS_NAME, "span10").text)

                             # Buscar los elementos <p> dentro del div con clase "span12" y unificar sus textos

                            contenido_parrafos = [parrafo.text for parrafo in post_element.find_elements(By.CSS_SELECTOR, ".span12 p")]
                            contenidoEvidencias.append(" ".join(contenido_parrafos))

                           

        return JsonResponse({'id_classroom':'2776992','status': 200,'date_end':element_fechaEntrega, 'names':element_name, 'content':contenidoEvidencias})

    else:
            # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
            # global_driver = initialize_driver()
            # global_driver.get(url+'init.php?muro=1')

            return JsonResponse({'status': 400, 'message': 'ERROR'})

#https://sena.territorio.la/perfil.php?id=31247202
#https://sena.territorio.la/tareas.php?clase=2776992
#https://sena.territorio.la/init.php?muro=1  clpost.php
#https://sena.territorio.la/tarea_tt.php?tarea=480296055 dependiendo de la tarea