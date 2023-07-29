from django.shortcuts import render
from django.http import HttpResponseRedirect

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
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
    if request.method == 'POST':
        identification = request.POST.get('identification')
        password = request.POST.get('pass')
        
        # Verificar la cuenta utilizando el dato de verificación
        if identification == '1234192477' and password == 'Colgate123456':
            # Código para realizar el inicio de sesión exitoso
            driver = webdriver.Chrome()
   
            driver.get('https://sena.territorio.la/index.php?login=true')
            usuario = driver.find_element("id","document")
            usuario.send_keys("1234192477")

            clave = driver.find_element("id","passwd")
            clave.send_keys("Colgate123456")
            clave.send_keys(Keys.ENTER)
    
            driver.get('https://sena.territorio.la/init.php')
            alert = Alert(driver)
            time.sleep(0.6)
            alert.accept()
            # elemento = driver.find_element(By.CLASS_NAME, "thumbnail")
            elemento = driver.find_element(By.XPATH, '//*[@id="catalogo-main-content"]')

            # Obtener el contenido HTML del elemento
            contenido_html = elemento.get_attribute('innerHTML')

            # Crear un objeto BeautifulSoup
            soup = BeautifulSoup(contenido_html, 'html.parser')
            elementos_con_clase = soup.find_all(lambda tag: tag.has_attr('class') and any('letras1' in clase for clase in tag['class']))
            contenido_class = [{'texto': elemento.get_text(), 'href': elemento.get('href')} for elemento in elementos_con_clase]

            return render(request, 'home.html',{'content':contenido_class})

    
        else:
            # Código para manejar el inicio de sesión fallido
            return HttpResponseRedirect('/login') #tedex@hotmail.com

    return HttpResponseRedirect('/login')