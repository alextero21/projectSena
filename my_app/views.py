from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from django.http import HttpResponse

# Ruta al controlador ChromeDriver
chrome_driver_path = 'C:\dchrome\chromedriver.exe'  # (o .exe en Windows)
import time




# from django.http import HttpResponse

# Create your views here.
def login(request):
    # return render(request, 'login.html')
    return render(request, 'login.html')
    # return HttpResponse('<h1>Hello world</h1>')

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