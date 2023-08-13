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
    global global_driver
    
   
    # Comprobar si el controlador está activo
    # if global_driver and is_driver_active(global_driver):

    if global_driver and is_driver_active(global_driver):
        # AQUI COMIENZA EL MURO

        # global_driver.get(url+'init.php?muro=1')
        global_driver.get('http://localhost:8000/probar')

  
        num_elementos_anteriores = 0
        # ultimo_array_valores = []
        unique_posts = set()
        unique_tarea_params = set()
        while True:
            # Esperar a que se carguen más elementos "post"
            WebDriverWait(global_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'post')]"))
            )

            post_elements = global_driver.find_elements(By.XPATH, "//div[starts-with(@id, 'post')]")
            
            if len(post_elements) == num_elementos_anteriores:
                # No hay nuevos elementos cargados, salir del ciclo
                break

            for post_element in post_elements:
                # Buscar las clases "nombres" dentro del elemento "post"
                nombres_elements = post_element.find_elements(By.CLASS_NAME, "nombres")
                for nombres_element in nombres_elements:
                    href = nombres_element.get_attribute("href")
                    parsed_url = urlparse(href)
                    grupo_param = parse_qs(parsed_url.query).get("grupo")
                    
                    if grupo_param and grupo_param[0] == "2776992":
                        # Buscar la clase "botonPersonalizadoBootstrap" dentro del elemento "post"
                        boton_elements = post_element.find_elements(By.CLASS_NAME, "botonPersonalizadoBootstrap")
                        for boton_element in boton_elements:
                            href_boton = boton_element.get_attribute("href")
                            parsed_url_boton = urlparse(href_boton)
                            tarea_param = parse_qs(parsed_url_boton.query).get("tarea")
                            if tarea_param:
                                tarea_value = tarea_param[0]  # Obtener el valor de tarea_param
                                unique_tarea_params.add(tarea_value)
                                # unique_posts.add(post_element.text)

            num_elementos_anteriores = len(post_elements)
            
            # Intentar ubicar y hacer clic en el botón "Ver más"
            try:
                ver_mas_button = global_driver.find_element(By.XPATH, "//a[contains(text(), 'Ver más')]")
                ver_mas_button.click()
            except NoSuchElementException:
                # Si no se encuentra el botón "Ver más", el ciclo ha terminado
                break

        # Convertir el conjunto de "unique_posts" en una lista
        # unique_posts_list = list(unique_posts)
        # for post_text in unique_posts_list:
        #     print(post_text)

        # Imprimir los valores únicos de tarea_param
        for tarea_param in unique_tarea_params:
            print(f"Valor único de tarea_param: {tarea_param}")



        # WebDriverWait(global_driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'post')]")))


        return JsonResponse({'status': 200, 'message': 'ABIERTO EL CONTROLADOR Y OBTENIDOS TODOS LOS POST'})

    else:
        # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
        global_driver = initialize_driver()
        # global_driver.get(url + 'index.php?login=true')
        global_driver.get('http://localhost:8000/probar')

        return JsonResponse({'status':200, 'message':'Abriendo controladorsssssssss'})
        # wait = WebDriverWait(global_driver, 10)

        # usuario = wait.until(EC.presence_of_element_located((By.ID, "document")))
        # contrasena = wait.until(EC.presence_of_element_located((By.ID, "passwd")))
        # usuario.send_keys(1234192477)
        # contrasena.send_keys('Colgate123456')

        # contrasena.send_keys(Keys.ENTER)     
    
        
    
def test(request):

    return render(request, 'test.html')


def getContent(request):

    global global_driver

    if global_driver and is_driver_active(global_driver):
            
        global_driver.get(url+'init.php?muro=1')

        num_elementos_anteriores = 0
        num_elementos_actuales = len(global_driver.find_elements(By.CSS_SELECTOR, "[id^='post']"))

        while num_elementos_actuales > num_elementos_anteriores:
            ver_mas_link = global_driver.find_element(By.XPATH, "//a[contains(text(), 'Ver más')]")
            posts = EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'post')]"))
            try:
                # Esperar a que el elemento sea interactable antes de hacer clic en él
                WebDriverWait(global_driver, 10).until(EC.element_to_be_clickable(ver_mas_link), posts)
                ver_mas_link.click()

                time.sleep(2)  # Dar tiempo para que los nuevos elementos se carguen
                num_elementos_anteriores = num_elementos_actuales
                num_elementos_actuales = len(global_driver.find_elements(By.CSS_SELECTOR, "[id^='post']"))

                # Obtener y mostrar el contenido de los elementos "post"
                post_elements = global_driver.find_elements(By.XPATH, "//div[starts-with(@id, 'post')]")
                for post_element in post_elements:

                    # Buscar las clases "nombres" dentro del elemento "post"
                    nombres_elements = post_element.find_elements(By.CLASS_NAME, "nombres")
                    for nombres_element in nombres_elements:
                        href = nombres_element.get_attribute("href")
                        parsed_url = urlparse(href)
                        grupo_param = parse_qs(parsed_url.query).get("grupo")#tarea=483078840

                        # if grupo_param and grupo_param[0] == "2776992":
                        #     print("Elemento con grupo 2776992:", post_element.text)

                         # Buscar la clase "botonPersonalizadoBootstrap" dentro del elemento "post"
                        boton_elements = post_element.find_elements(By.CLASS_NAME, "botonPersonalizadoBootstrap")
                        for boton_element in boton_elements:
                            href_boton = boton_element.get_attribute("href")
                            parsed_url_boton = urlparse(href_boton)
                            tarea_param = parse_qs(parsed_url_boton.query).get("tarea")
                            
                            if grupo_param and grupo_param[0] == "2776992" and tarea_param:
                                print("Elemento con grupo 2776992 y tarea:", post_element.text)


            except:
                # Si el elemento ya no es interactable, salir del bucle
                break

        WebDriverWait(global_driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'post')]")))


        return JsonResponse({'status': 200, 'message': 'ABIERTO EL CONTROLADOR Y OBTENIDOS TODOS LOS POST'})

    else:
            # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
            # global_driver = initialize_driver()
            # global_driver.get(url+'init.php?muro=1')

            return JsonResponse({'status': 400, 'message': 'ERROR'})


#https://sena.territorio.la/perfil.php?id=31247202
#https://sena.territorio.la/tareas.php?clase=2776992
#https://sena.territorio.la/init.php?muro=1  clpost.php
#https://sena.territorio.la/tarea_tt.php?tarea=480296055 dependiendo de la tarea