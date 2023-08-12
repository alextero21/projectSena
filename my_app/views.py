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
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from django.http import JsonResponse

global_driver = None
url = 'https://sena.territorio.la/'
# Ruta al controlador ChromeDriver
# chrome_driver_path = 'C:\dchrome\chromedriver.exe'  # (o .exe en Windows)



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

def testing(request):
    # Obtener los datos enviados en la solicitud AJAX

    

    return render(request, 'test.html')
    
    
# Variable para mantener el estado de la interacción
ver_mas_realizado = False

def getTesting(request):
    global global_driver

    # Comprobar si el controlador está activo
    if global_driver and is_driver_active(global_driver):
        global_driver.get("http://localhost:8000/test#")

        num_elementos_anteriores = 0
        num_elementos_actuales = len(global_driver.find_elements(By.CSS_SELECTOR, "[id^='post']"))

        while num_elementos_actuales > num_elementos_anteriores:
            ver_mas_link = global_driver.find_element(By.XPATH, "//a[contains(text(), 'Ver más')]")
            try:
                # Esperar a que el elemento sea interactable antes de hacer clic en él
                WebDriverWait(global_driver, 10).until(EC.element_to_be_clickable(ver_mas_link))
                ver_mas_link.click()

                time.sleep(2)  # Dar tiempo para que los nuevos elementos se carguen
                num_elementos_anteriores = num_elementos_actuales
                num_elementos_actuales = len(global_driver.find_elements(By.CSS_SELECTOR, "[id^='post']"))
            except:
                # Si el elemento ya no es interactable, salir del bucle
                break


        print(num_elementos_actuales)
        return JsonResponse({'status': 200, 'message': 'ABIERTO EL CONTROLADOR Y OBTENIDOS TODOS LOS POST'})

    else:
        # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
        global_driver = initialize_driver()
        global_driver.get("http://localhost:8000/test")

        return JsonResponse({'status': 200, 'message': 'Abriendo controlador'})



def getContent(request):

    global global_driver

    if global_driver and is_driver_active(global_driver):
            
        global_driver.get(url+'init.php?muro=1')
        
        

      # Obtener el número de elementos del catálogo actuales
        num_elementos_anteriores = len(global_driver.find_elements(By.CSS_SELECTOR, "[id^='post']"))

        # Ejecutar la función verMas()
        ver_mas_link = global_driver.find_element(By.XPATH, "//a[contains(text(), 'Ver más')]")
        ver_mas_link.click()

        wait = WebDriverWait(global_driver, 10)
        # Esperar a que los elementos anteriores se vuelvan obsoletos
        wait.until(EC.staleness_of(global_driver.find_elements(By.CSS_SELECTOR, "[id^='post']")))

        # Esperar hasta que se carguen nuevos elementos
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "[id^='post']")) > num_elementos_anteriores)

        # Realizar operaciones con los nuevos elementos del catálogo
        nuevos_elementos = global_driver.find_elements(By.CSS_SELECTOR, "[id^='post']")
        for elemento in nuevos_elementos:
            # Procesar los nuevos elementos como desees
            pass

    

    return JsonResponse({'status':200, 'message':'Excelente','url':'test'})


#https://sena.territorio.la/perfil.php?id=31247202
#https://sena.territorio.la/tareas.php?clase=2776992
#https://sena.territorio.la/init.php?muro=1  clpost.php
#https://sena.territorio.la/tarea_tt.php?tarea=480296055 dependiendo de la tarea