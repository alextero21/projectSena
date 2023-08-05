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

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

global_driver = None
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
    url = 'https://sena.territorio.la/'
    # Comprobar si el controlador está activo
    if global_driver and is_driver_active(global_driver):
        # Continuar interactuando con el navegador ya abierto
        user = request.POST.get('user')
        password = request.POST.get('pass')
        global_driver.get(url + 'index.php?login=true')
        wait = WebDriverWait(global_driver, 10)

        if request.POST.get('pagina'):
            contentSena= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="catalogo-main-content"]')))
            contenido_html = contentSena.get_attribute('innerHTML')
            soup = BeautifulSoup(contenido_html, 'html.parser')
            elementos_con_clase = soup.find_all(lambda tag: tag.has_attr('class') and 'letras1' in tag['class'])
            contenido_class = [{'url':url,'texto': elemento.get_text(), 'href': elemento.get('href').replace('?', '%3F').replace('=', '%3D')} for elemento in elementos_con_clase]
            print(contenido_class)
            # global_driver.get(url + 'perfil.php?id=31247202')
           
            # enlace.click()
            
        else:
            
            usuario = wait.until(EC.presence_of_element_located((By.ID, "document")))
            contrasena = wait.until(EC.presence_of_element_located((By.ID, "passwd")))
            usuario.send_keys(user)
            contrasena.send_keys(password)

            contrasena.send_keys(Keys.ENTER)

        
        # Acceder a los datos enviados en la solicitud POST
            # key1_value = request.POST.get('pagina')


            # contentSena= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="catalogo-main-content"]')))
            # contenido_html = contentSena.get_attribute('innerHTML')
            
            #https://sena.territorio.la/perfil.php?id=31247202



        return HttpResponse("Navegador ya abierto y controlador disponible.")
    else:
        # Si el controlador no está activo o no está inicializado, inicializarlo nuevamente
        global_driver = initialize_driver()
        global_driver.get(url + 'index.php?login=true')

        # ... Resto de la lógica ...

        return HttpResponse("Navegador abierto y controlador inicializado.")


def verify(request):
    # if request.method == 'POST':
    #     identification = request.POST.get('identification')
    #     password = request.POST.get('pass')
        
    #     # Verificar la cuenta utilizando el dato de verificación
    #     if identification == '1234192477' and password == 'Colgate123456':
            # Código para realizar el inicio de sesión exitoso
    driver = webdriver.Chrome()
    url='https://sena.territorio.la/'
   
    driver.get(url+'index.php?login=true')
    usuario = driver.find_element("id","document")
    usuario.send_keys("1234192477")

    clave = driver.find_element("id","passwd")
    clave.send_keys("Colgate123456")
    clave.send_keys(Keys.ENTER)
    
    driver.get(url+'init.php')
    alert = Alert(driver)
    time.sleep(0.6)
    alert.accept()
    
    # driver.get(url+'init.php')
    elemento = driver.find_element(By.XPATH, '//*[@id="catalogo-main-content"]')

    # Obtener el contenido HTML del elemento
    contenido_html = elemento.get_attribute('innerHTML')

    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(contenido_html, 'html.parser')
    elementos_con_clase = soup.find_all(lambda tag: tag.has_attr('class') and any('letras1' in clase for clase in tag['class']))
    contenido_class = [{'url':url,'texto': elemento.get_text(), 'href': elemento.get('href').replace('?', '%3F').replace('=', '%3D')} for elemento in elementos_con_clase]


    # Obtener la cookie del driver
    mi_cookie = driver.get_cookies()
    driver.quit()
    # cookies.quit()

    # driver2= webdriver.Chrome()

    # for cookie in cookies:
    #     driver2.add_cookie(cookie)
    response = render(request, 'home.html', {'content': contenido_class})
    response.set_cookie('cookie2', mi_cookie)

    return response

    
        # else:
        #     # Código para manejar el inicio de sesión fallido
        #     return HttpResponseRedirect('/login') #tedex@hotmail.com

    # return HttpResponseRedirect('/login')

def get_cookies(request,href):

    # return render(request, 'home.html')
   

    return render(request, 'test.html',{'url':href})