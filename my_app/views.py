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
import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from django.http import JsonResponse

global_driver = None
url = 'https://sena.territorio.la/'
# Ruta al controlador ChromeDriver
chrome_driver_path = 'C:\dchrome\chromedriver.exe'  # (o .exe en Windows)



import time



def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))





def login(request):

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
def activateDriver(request):
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
            
            



def home(request):


    
    # driver.get(url+'init.php')
    # alert = Alert(driver)
    # time.sleep(0.6)
    # alert.accept()


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
        return render(request, 'test.html')

    # return HttpResponseRedirect('/login')

def get_url(request,href):

    if global_driver and is_driver_active(global_driver):
        
        global_driver.get(url+href)

        return JsonResponse({'status':200, 'message':'Excelente','url':'test'})
    else:
      return JsonResponse({'status':404, 'message':'Error en el navegador','url':'home'})

def proxy_view(request):
    # Obtener los datos enviados en la solicitud AJAX

    data = "methodclave=registroclave&idgrupo=31247202"

    referer = request.META.get('HTTP_REFERER', '')

    # Configurar las cabeceras necesarias para la solicitud al servidor remoto
    headers = {
        'User-Agent': request.META.get('HTTP_USER_AGENT', ''),
        'Referer': referer,
        # ... otras cabeceras ...
    }

    response = requests.post('https://sena.territorio.la/webservices/grupo.php', data=data, headers=headers)

    try:
        json_data = response.json()
        proxy_response = JsonResponse(json_data, status=response.status_code)
    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        error_message = {'error': 'Error al decodificar JSON en la respuesta'}
        proxy_response = JsonResponse(error_message, status=500)


    proxy_response['Access-Control-Allow-Origin'] = '*'  # Permitir todas las solicitudes (cambiar según tus necesidades)

    print(proxy_response)

    return proxy_response
    
#https://sena.territorio.la/perfil.php?id=31247202
#https://sena.territorio.la/tareas.php?clase=2776992
#https://sena.territorio.la/init.php?muro=1  clpost.php
#https://sena.territorio.la/tarea_tt.php?tarea=480296055 dependiendo de la tarea