from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager #No entiendo porque aparece como inhabilitado, pero si lo toma cuando lo referencio mas adelante
import time

# 1. AQUI GENERO LA CONFIGURACION DEL NAVEGADOR
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
wait = WebDriverWait(driver, 25)

try:
    print("Iniciando automatizacion en uTest...")
    driver.get("https://www.utest.com/")

    # Clic inicial para abrir el formulario
    btn_join = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Join Now')]")))
    btn_join.click()
    print("Clic en inicio de registro exitoso.")

    # 2. PASO A LA PESTAÑA QUE SE ABRE LUEGO DE DAR CLIC EN JOIN NOW
    time.sleep(5)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        print("Cambiado a la pestaña del formulario.")

    # 3. LLENADO DE DATOS PERSONALES EN EL FORMULARIO MENOS LA LISTA DESPLEGABLE DE COUNTRY
    print("Completando campos obligatorios...")
    
    # First Name
    first_name = wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
    first_name.send_keys("Andres")
    
    # Last Name
    driver.find_element(By.ID, "lastName").send_keys("Garcia")
    
    # Email
    driver.find_element(By.ID, "email").send_keys("andres.qa.test2026@example.com")

    # Fecha de nacimiento (MI FECHA DE CUMPLEAÑOS REAL :)) 
    driver.find_element(By.ID, "birthMonth").send_keys("September")
    driver.find_element(By.ID, "birthDay").send_keys("16")
    driver.find_element(By.ID, "birthYear").send_keys("1999")
    
    print("Datos de identidad completados.")

    # 4. CONSENTIMIENTOS CON CASILLAS DE VERIFICACION PARA PODER HABILITAR DEL BTN DE CREATE ACOUNT
    print("Marcando casillas de consentimiento...")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    for box in checkboxes:
        driver.execute_script("arguments[0].click();", box)

    # 5. CLIC EN EL BOTON AMARILLO (CREATE ACCOUNT)
    print("Buscando el boton amarillo btn-create-account...")
    
    # Usamos la clase exacta que Encontramos haciendo la inspeccion de la pagina, ya que en el front esta escrito diferente a como se encuentra en el codigo de inspeccion ( esto me retraso bastante ya que hice muchas pruebas y no pasaba los primeros datos por este error)
    try:
        # Esperamos a que el boton este presente
        btn_final = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-create-account")))
        
        # Scroll para asegurar que el boton sea visible , ya que se sobrepone la ventana de aceptar las cookies )
        driver.execute_script("arguments[0].scrollIntoView();", btn_final)
        time.sleep(2)
        
        # Forzamos el clic con JavaScript para asegurar la ejecucion ( este fracmento lo tome de Ejemplos de proyectos que realice con tripleten)
        driver.execute_script("arguments[0].click();", btn_final)
        print("Boton Create Account presionado exitosamente.")
        
    except Exception as e:
        print(f"No se pudo interactuar con el boton final: {str(e)}")

    print("Automatizacion terminada con exito.")
    time.sleep(5)

finally:
    print("Cerrando navegador...")
    driver.quit()