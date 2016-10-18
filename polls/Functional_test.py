from unittest import TestCase

from pip._vendor.distlib.compat import raw_input
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
import os


class FunctionalTest(TestCase):
    def set_text(self, key, string):
        nombre = self.browser.find_element_by_id(key)
        nombre.clear()
        nombre.send_keys(string)

    def set_click(self, key):
        link = self.browser.find_element_by_id(key)
        link.click()

    def assertText(self, xpath, expected):
        html = self.browser.find_element_by_xpath(xpath)
        self.assertIn(expected, html.text)

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8000')

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.assertIn('BuscoAyuda', self.browser.title)

    def test_registro(self):
        self.set_click('id_register')
        self.browser.implicitly_wait(2)
        self.set_text('id_nombre', 'Gloria')
        self.set_text('id_apellidos', 'Cortez')
        self.set_text('id_aniosExperiencia', '5')
        tipo_servicio = "//select[@id='id_tiposDeServicio']/option[text()='Desarrollador Web']"
        self.browser.find_element_by_xpath(tipo_servicio).click()
        self.set_text('id_telefono', '3173024578')
        self.set_text('id_correo', 'correo@hotmail.com')
        self.set_text('id_imagen',  os.path.join(os.getcwd(), 'test_resources', 'piton.jpg'))
        self.set_text('id_username', 'gcortes')
        self.set_text('id_password', 'clave123')
        self.set_click('id_grabar')
        self.browser.implicitly_wait(3)
        self.assertText('//span[text()="Gloria Cortez"]', "Gloria Cortez")

    def test_detalle(self):
        self.browser.find_element_by_xpath('//span[text()="Gloria Cortez"]').click()
        self.browser.implicitly_wait(2)
        self.assertText('//h2[text()="Gloria Cortez"]', 'Gloria Cortez')
        self.assertText('//h4[contains(text(),"5 años")]', '5 años')
        self.assertText('//h4[contains(text(),"3173024578")]', '3173024578')
        self.assertText('//h4[contains(text(),"correo@hotmail.com")]', 'correo@hotmail.com')

    def test_login(self):
        self.set_click('id_login')
        self.browser.implicitly_wait(3)
        self.set_text('login-username', 'gcortes')
        self.set_text('login-password', 'clave123')
        self.set_click('id_entrar')
        self.assertText('//a[contains(text()," Logout")]', "Logout")

    def test_editar_perfil(self):
        self.test_login()
        self.browser.implicitly_wait(3)
        self.set_click('id_editar')
        self.browser.implicitly_wait(3)
        self.set_text('id_aniosExperiencia', '7')
        self.set_text('id_telefono', '43214143')
        self.set_text('id_correo', 'otrocorreo@hotmail.com')
        self.set_text('id_imagen', os.path.join(os.getcwd(), 'test_resources', 'piton2.jpg'))
        self.set_click('id_grabar')
        self.browser.implicitly_wait(5)
        self.assertText('//a[contains(text()," Logout")]', "Logout")

    def test_comentario(self):
        self.browser.get('http://localhost:8000')
        link = self.browser.find_element_by_link_text('Gloria Cortez')
        link.click()

        self.browser.implicitly_wait(5)
        correo = self.browser.find_element_by_id('correo')
        correo.send_keys('correocomentario@gmail.com')

        comentario = self.browser.find_element_by_id('comentario')
        texto_comentario = 'Soy un comentario '
        comentario.send_keys(texto_comentario)
        boton_grabar = self.browser.find_element_by_xpath('//form[1]/button[1]')
        boton_grabar.click()

        h4 = self.browser.find_element_by_xpath('//h4[text()="correocomentario@gmail.com"]')
        self.assertIn('correocomentario@gmail.com', h4.text)

        p = self.browser.find_element_by_xpath('//p[text()="%s"]' % texto_comentario)
        self.assertIn(texto_comentario, p.text)