import unittest
from selenium import webdriver
import time

class TestAddPoliticalParty(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()

        
        
    def test_create(self):
        #Realizamos login, con las credenciales a continuacion
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("user1")
        self.driver.find_element_by_id('id_password').send_keys("decide2020")
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        #Añadimos una pequeña pausa para que el navegadpr no se sature
        time.sleep(1)
        #Clickamos en el botón añadir partido político
        self.driver.find_element_by_link_text("Political partys").click()
        self.driver.find_element_by_css_selector('a.addlink').click()

        #Añadimos todos los campos necesarios para poder guardar un partido politico

        self.driver.find_element_by_id('id_name').send_keys('Partido de Selenium')
        self.driver.find_element_by_id('id_acronym').send_keys('PSM')
        self.driver.find_element_by_id('id_description').send_keys('Una descripción válida')
        self.driver.find_element_by_id('id_headquarters').send_keys('Madrid')
        self.driver.find_element_by_id('id_image').send_keys('http://estoesunapruebadeselenium.com')

        # una vez introducimos la informacion añadimos al partido
        self.driver.find_element_by_css_selector('input.default').click()
        # obtenemos finalmente el mensaje de que el partido se ha creado bien finalmente
        self.assertTrue(len(self.driver.find_elements_by_class_name('success'))>0) 
        

    def test_edit(self):
        #Realizamos login, con las credenciales a continuacion
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("user1")
        self.driver.find_element_by_id('id_password').send_keys("decide2020")
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        #Añadimos una pequeña pausa para que el navegadpr no se sature
        time.sleep(1)
        #Clickamos en el botón añadir partido político
        self.driver.find_element_by_link_text("Political partys").click()
        self.driver.find_element_by_css_selector('a.addlink').click()

        #Añadimos todos los campos necesarios para poder guardar un partido politico

        self.driver.find_element_by_id('id_name').send_keys('Partido de Selenium 2')
        self.driver.find_element_by_id('id_acronym').send_keys('PSM 2')
        self.driver.find_element_by_id('id_description').send_keys('Una descripción válida 2')
        self.driver.find_element_by_id('id_headquarters').send_keys('Sevilla')
        self.driver.find_element_by_id('id_image').send_keys('http://estoesunaprueba.com')

        # una vez introducimos la informacón guardamos el partido en cuestión y decimos cambiar su nombre
        self.driver.find_element_by_name('_continue')

        #cambiamos el nombre del partido
        self.driver.find_element_by_id('id_name').send_keys('edited')

        #posteriormente guardamos para ver qeu se ha editado el partido en cuestion
        self.driver.find_element_by_css_selector('input.default').click()
        # obtenemos finalmente el mensaje de que el partido se ha creado bien finalmente
        self.assertTrue(len(self.driver.find_elements_by_class_name('success'))>0) 

    def test_bad_edit(self):
        #Realizamos login, con las credenciales a continuacion
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("user1")
        self.driver.find_element_by_id('id_password').send_keys("decide2020")
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        #Añadimos una pequeña pausa para que el navegadpr no se sature
        time.sleep(1)
        #Clickamos en el botón añadir partido político
        self.driver.find_element_by_link_text("Political partys").click()
        self.driver.find_element_by_css_selector('a.addlink').click()

        #Añadimos todos los campos necesarios para poder guardar un partido politico

        self.driver.find_element_by_id('id_name').send_keys('Partido de Selenium')
        self.driver.find_element_by_id('id_acronym').send_keys('PSM')
        self.driver.find_element_by_id('id_headquarters').send_keys('Madrid')
        self.driver.find_element_by_id('id_description').send_keys('Una descripción válida')
        self.driver.find_element_by_id('id_image').send_keys('http://estoesunapruebadeselenium.com')

        # una vez introducimos la informacion añadimos al partido
        self.driver.find_element_by_css_selector('input.default').click()
        # obtenemos el mesaje de error al ejecutar intenetar insertar un partido con la misma descripción y nombre
        self.assertTrue(len(self.driver.find_elements_by_class_name('errornote'))>0)    

    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()

