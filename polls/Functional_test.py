from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import os


def set_text(self, key, string):
    nombre = self.browser.find_element_by_id(key)
    nombre.send_keys(string)


def set_click(self, key):
    link = self.browser.find_element_by_id(key)
    link.click()


class FunctionalTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('BuscoAyuda', self.browser.title)

    def test_registro(self):
        self.browser.get('http://localhost:8000')
        set_click(self, 'id_register')
        self.browser.implicitly_wait(2)

        set_text(self, 'id_nombre', 'Gloria')
        set_text(self, 'id_apellidos', 'Cortez')
        set_text(self, 'id_aniosExperiencia', '5')
        self.browser.find_element_by_xpath(
            "//select[@id='id_tiposDeServicio']/option[text()='Desarrollador Web']").click()
        set_text(self, 'id_telefono', '3173024578')
        set_text(self, 'id_correo', 'correo@hotmail.com')
        set_text(self, 'id_imagen',  os.path.join(os.getcwd(), 'test_resources', 'piton.jpg'))
        set_text(self, 'id_username', 'gcortes')
        set_text(self, 'id_password', 'clave123')
        set_click(self, 'id_grabar')
        self.browser.implicitly_wait(3)
        span = self.browser.find_element(By.XPATH, '//span[text()="Gloria Cortez"]')

        self.assertIn("Gloria Cortez", span.text)

    def test_detalle(self):
        self.browser.get('http://localhost:8000')
        span = self.browser.find_element_by_xpath('//span[text()="Gloria Cortez"]')
        span.click()

        self.browser.implicitly_wait(2)

        h2 = self.browser.find_element_by_xpath('//h2[text()="Gloria Cortez"]')
        self.assertIn('Gloria Cortez', h2.text)

        experiencia = self.browser.find_element_by_xpath('//h4[contains(text(),"5 años")]')
        self.assertIn('5 años', experiencia.text)

        telefono = self.browser.find_element_by_xpath('//h4[contains(text(),"3173024578")]')
        self.assertIn('3173024578', telefono.text)

        correo = self.browser.find_element_by_xpath('//h4[contains(text(),"correo@hotmail.com")]')
        self.assertIn('correo@hotmail.com', correo.text)