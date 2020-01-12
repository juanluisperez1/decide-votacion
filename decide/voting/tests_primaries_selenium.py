import unittest
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

class TestAddPoliticalParty(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()

        
        
    def test_create_senate_primary_and_make_senator(self):

        #login in decide
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("user1")
        self.driver.find_element_by_id('id_password').send_keys("decide2020")
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(1)
       
        # Add a new voting
        self.driver.find_element_by_link_text("Votings").click()
        self.driver.find_element_by_css_selector('a.addlink').click()

        #We added all the necessary fields to be able to save the voting
        self.driver.find_element_by_id('id_name').send_keys('Senador PP')

        
        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text("¿quien quieres que sea un senador del partido popular?")

        select = Select(self.driver.find_element_by_id('id_tipe'))
        select.select_by_visible_text("Senate primaries")
        
        select = Select(self.driver.find_element_by_id('id_political_party'))
        select.select_by_visible_text("partido popular")

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text("http://localhost:8000")
        time.sleep(1)
        # Save
        self.driver.find_element_by_css_selector('input.default').click()
        
        # We check that it has been stored correctly
        self.assertTrue(len(self.driver.find_elements_by_class_name('success'))>0) 

        self.driver.find_element_by_class_name('action-select').click()
        select = Select(self.driver.find_element_by_name('action'))
        select.select_by_visible_text("Start")
        self.driver.find_element_by_class_name('button').click()
        time.sleep(35)
        self.driver.find_element_by_class_name('action-select').click()
        select = Select(self.driver.find_element_by_name('action'))
        select.select_by_visible_text("Stop")
        self.driver.find_element_by_class_name('button').click()
        time.sleep(30)
        self.driver.find_element_by_class_name('action-select').click()
        select = Select(self.driver.find_element_by_name('action'))
        select.select_by_visible_text("Tally")
        self.driver.find_element_by_class_name('button').click()
        time.sleep(35)
        
        self.driver.find_element_by_link_text('Home').click()
        self.driver.find_element_by_link_text("User profiles").click()
        self.driver.find_element_by_link_text("(M,2000-01-11,partido popular)").click()
        time.sleep(3)
        senator=self.driver.find_element_by_id("id_employment").get_attribute(name='value')
        self.assertTrue(senator == 'S')

    
    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()
