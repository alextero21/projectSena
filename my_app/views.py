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
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import NoSuchElementException
from django.core.files.storage import default_storage
import os
from django.conf import settings

global_driver = None
url = 'https://sena.territorio.la/'
url_perfil_id = 'perfil.php?id=31247202'
# Ruta al controlador ChromeDriver
# chrome_driver_path = 'C:\dchrome\chromedriver.exe'  # (o .exe en Windows)



import time



def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))





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
        global_driver = initialize_driver()
        global_driver.get(url + 'index.php?login=true')

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



    data = [       {
            "id_classroom": "6726881",
            "classroom": "Inglés",
            "status": 200,
            "materia": [
                "Inglés",
                "Inglés",
                "Inglés",
            ],
            "id_tarea": [
                "400126367",
                "468567762",
                "449956361",
            ],
            "date_end": [
                "Fecha de entrega: 2023-07-30 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-08-04 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-08-12 14:45:00\nArchivos:\nResponder Evidencia",
            ],
            "names": [
                "EIKA YILIETH PEREZ",
                "EIKA YILIETH PEREZ",
                "EIKA YILIETH PEREZ",

            ],
            "content": [
                "Buenas tardes. Por favor subir la actividad desarrollada en el ambiente de aprendizaje",
                "Subir la tarea de ingles que si no sabes es esta que te voy a mostrar a continuacion",
                "Los dibujos didacticos que te di tienen que ser diferentes y por eso el grupo debe de saber cual es",
                
            ]
                
        },

        {    
            "id_classroom": "2776992",
            "classroom": "Técnico en Servicios Comerciales y Financieros",
            "status": 200,
            "materia": [
                "Asesorar consumidor Financiero",
                "Derechos fundamentales",
                "Derechos fundamentales",
                "Derechos fundamentales",
                "Razonamiento cuantitativo",
                "Derechos fundamentales",
                "Manejar Recursos Financieros",
                "Derechos fundamentales",
                "Derechos fundamentales",
                "Derechos fundamentales",
                "Derechos fundamentales",
            ],
            "id_tarea": [
                "483078840",
                "479413805",
                "476003090",
                "472620361",
                "470634816",
                "468648314",
                "464688279",
                "459774401",
                "456193106",
                "452513904",
                "497907367",
            ],
            "date_end": [
                "Fecha de entrega: 2023-08-12 14:45:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-08-04 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-07-30 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-07-26 13:00:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-07-21 11:42:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-07-16 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-07-26 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-07-07 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-06-24 23:30:00\nArchivos:\nTRABAJOnYnCIUDADANnnA.mp4\nCARTILLAnEMPLEOnRETORNOnopn3ncompletonbajan11n10n2017.pdf\nResponder Evidencia",
                "Fecha de entrega: 2023-06-19 23:30:00\nArchivos:\nResponder Evidencia",
                "Fecha de entrega: 2023-06-13 23:30:00\nArchivos:\nResponder Evidencia"
            ],
            "names": [
                "MARIA ELENA MONTUFAR MUÑOZ",
                "JORGE ELIECER VERA TASAMA",
                "JORGE ELIECER VERA TASAMA",
                "JORGE ELIECER VERA TASAMA",
                "YULIETH JARAMILLO OSPINA",
                "JORGE ELIECER VERA TASAMA",
                "EDGAR DE JESUS ARENAS VARGAS",
                "JORGE ELIECER VERA TASAMA",
                "JORGE ELIECER VERA TASAMA",
                "JORGE ELIECER VERA TASAMA",
                "JORGE ELIECER VERA TASAMA"
            ],
            "content": [
                "Buenas tardes. Por favor subir la actividad desarrollada en el ambiente de aprendizaje",
                "   RAP:     Participar en acciones solidarias   D F T -Espacio para carga de la evidencia 2 Guía 4 Derechos Fundamentales-Los DESC     Apreciado Aprendiz   Se activa el espacio para la carga de evidencia 2 correspondiente a la guía 4 Actividad 2   Evidencia a cargar:  “Derechos económicos sociales y culturales” ",
                " RAP: Participar en acciones solidarias teniendo en cuenta el ejercicio de los derechos humanos, de los pueblos y de la naturaleza.   Apreciad@ Aprendiz   Se activa el espacio para la carga de evidencia1 correspondiente a la guía 4 Actividad 1   Evidencia a cargar:  “Estado social de derecho y la desprotección legal ” ",
                "        RAP: Practicar los derechos fundamentales en el trabajo   Asunto: E D F T y C L -Espacio para carga de la evidencia 2 Guía 3 - Herramientas Jurídicas para reclamar el derecho- Derechos Fundamentales   Apreciado Aprendiz Se activa el espacio para la carga de evidencias correspondiente a la guía 3 Actividad 2   Evidencia por cargar: “Herramientas Jurídicas para reclamar el derecho ”   ",
                " Aquí enviaras los talleres de: -Figuras geométricas áreas, perímetros y volúmenes - Teorema de Pitágoras - Funciones Trigonométricas, en total son 3 archivos para enviar como evidencia de tu trabajo en clase. ",
                "   RAP: Practicar los derechos fundamentales en el trabajo de acuerdo con la Constitución Política y los Convenios Internacionales.   Apreciado Aprendiz Se activa el espacio para la carga de evidencias correspondiente a la guía 3 Actividad 1   Evidencia por cargar: “artículos constitucionales relacionados con los derechos del trabajador” ",
                " Elaborar un guion escrito para realizar una simulación donde se identifiquen las características, los tipos de servicios, las tarifas y condiciones del proceso vistos durante la guía. La simulación se realizará en clase para presentar a sus compañeros e instructor. ",
                " RAP: Valorar la importancia de la ciudadanía laboral Apreciado Aprendiz Se activa el espacio para la carga de evidencia 2- Derecho colectivo del trabajo- correspondiente a la guía 2 Actividad 2.   Producto evidencia a cargar: “Derecho laboral colectivo” ",
                " RAP: Valorar la importancia de la ciudadanía laboral Apreciado Aprendiz Se activa el espacio para la carga de evidencia 1 correspondiente a la guía 2 Actividad 1. Producto evidencia a cargar: Derecho laboral individual y Ciudadanía Laboral. Recordar que el producto debe socializarse. ",
                " RAP: Reconocer el trabajo como factor de movilidad social Apreciado Aprendiz Se activa el espacio para la carga de evidencias 2-Actividad 2 correspondiente a la guía 1. Evidencia por cargar: “La Dignidad Humana y Cambios en el Mundo del Trabajo” ",
                " RAP1: Reconocer el trabajo como factor de movilidad social y transformación vital, con referencia a la fenomenología y a los derechos fundamentales en el trabajo. Apreciado Aprendiz Se activa el espacio para la carga de evidencia 1 correspondiente a la guía 1. Evidencia a cargar: “Evolución del trabajo y su fenomenología” “FUNDAMENTOS DE ECONOMIA”  "
            ]
                
        }
]


    # return render(request, 'test.html')
    return JsonResponse({'data': data})


def getContent(request):

    global global_driver

    if global_driver and is_driver_active(global_driver):
            
        # AQUI COMIENZA EL MURO

        global_driver.get(url+'init.php?muro=1')
        # global_driver.get('http://localhost:8000/probar')

  
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