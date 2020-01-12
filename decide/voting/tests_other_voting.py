import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class TestAddVotingOther(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def test_createOther(self):
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        window_before = self.driver.window_handles[0]
        self.driver.find_element_by_id('id_username').send_keys("user1")
        self.driver.find_element_by_id('id_password').send_keys("decide2020")
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Votings").click()
        self.driver.find_element_by_css_selector('a.addlink').click()

        self.driver.find_element_by_id('id_name').send_keys('Encuesta definitiva')
        self.driver.find_element_by_id('id_desc').send_keys('Vamos a realizar una votacion publica para conocer la opinion del pueblo')

        self.driver.find_element_by_id('add_id_question').click()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to_window(window_after)
        time.sleep(1)
        self.driver.find_element_by_id('id_desc').send_keys('¿Nos vemos en septiembre definitivo?')
        self.driver.find_element_by_id('id_yes_no_question').click()
        self.driver.find_element_by_css_selector('input.default').click()
        self.driver.switch_to_window(window_before)
        time.sleep(1)

        select = Select(self.driver.find_element_by_id('id_tipe'))
        select.select_by_visible_text("Other")

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text("http://localhost:8000")

        self.driver.find_element_by_css_selector('input.default').click()

        self.assertTrue(len(self.driver.find_elements_by_class_name('success'))>0)

    def test_createQuestionOther(self):
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("user1")
        self.driver.find_element_by_id('id_password').send_keys("decide2020")
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Questions").click()

        self.driver.find_element_by_css_selector('a.addlink').click()

        self.driver.find_element_by_id('id_desc').send_keys('¿Nos vemos el 31 o aprobamos antes?')
        self.driver.find_element_by_id('id_yes_no_question').click()
        self.driver.find_element_by_css_selector('input.default').click()

        self.assertTrue(len(self.driver.find_elements_by_class_name('success'))>0)

    def test_editOther(self):
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("user1")
        self.driver.find_element_by_id('id_password').send_keys("decide2020")
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Votings").click()

        self.driver.find_element_by_link_text("Encuesta definitiva").click()

        self.driver.find_element_by_id('id_name').clear()
        time.sleep(1)
        self.driver.find_element_by_id('id_name').send_keys('Encuesta 2.0 definitiva')
        self.driver.find_element_by_id('id_desc').clear()
        time.sleep(1)
        self.driver.find_element_by_id('id_desc').send_keys('Vamos a cambiar la votacion publica por un error en la pregunta')
        
        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text("¿Nos vemos el 31 o aprobamos antes?")

        self.driver.find_element_by_css_selector('input.default').click()

        self.assertTrue(len(self.driver.find_elements_by_class_name('success'))>0)


    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()
