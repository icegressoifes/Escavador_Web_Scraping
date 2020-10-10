from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date, datetime, timedelta
from . import remove_caracter
import time
import logging
import sys
import pickle
import os
import random
import re

def f_logout(driver=None):
    
    driver.get("https://www.escavador.com/logout");
    time.sleep(5)
    try:    
        element_body = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'html')))
        element_select =  driver.execute_script("return arguments[0].querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog').querySelector('#clearFromBasic').shadowRoot.querySelector('#dropdownMenu');", element_body)
        list_element_option = element_select.find_elements_by_tag_name("option")
        for element_option in  list_element_option:
            element_option.click()
        driver.execute_script("arguments[0].querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog').querySelector('#clearBrowsingDataConfirm').click()", element_body)
    except:
        pass

def f_login(driver=None, user=None, password=None):
    f_logout(driver)
    time.sleep(4)
    driver.get("https://www.escavador.com/login")             

    print("\n>>> Página Acessada: ", driver.title)    
    element_form = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'login-form')))
    element_input_email = element_form.find_element_by_id("email")
    element_input_senha = element_form.find_element_by_id("senha")
    element_button_submit = element_form.find_element_by_tag_name("button")    
    
    actions = ActionChains(driver)
    actions.pause( 2 )
    actions.move_to_element(element_input_email)
    actions.double_click(element_input_email)
    actions.pause(2)
    actions.send_keys(user)
    actions.pause(2)
    actions.move_to_element(element_input_senha)
    actions.double_click(element_input_senha)
    actions.pause(2)
    actions.send_keys(password)
    actions.pause(2)
    actions.send_keys(Keys.RETURN)
    actions.perform()
      
    try:
        element_span_user = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'c-user-avatar__title')))
        print("\nSucesso ao realizar o login")
    except:
        print("\nFalha ao realizar o login")
        raise 
    
    time.sleep(14) 

def f_get_link(driver=None, name_person=None, whole_name=None, sex=None):
    list_content = []
    total_links = set([])
    quantity_found = 0
    cont_page = 4
    name_without_accent = remove_caracter.removerAcentosECaracteresEspeciais(name_person)
    whole_name_accent = remove_caracter.removerAcentosECaracteresEspeciais(whole_name)
    try:
        url = "https://www.escavador.com/busca?q={}&qo=p&f[pt][0]=curriculo".format(name_person)
        continuar = True
        driver.get(url)
        while continuar:
            print("\n\n>>> Página Acessada: ", driver.title)
            print(">>> URL Acessada: ", driver.current_url)
            element = None
            try:
                element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="escavador-app"]/div[1]/p[1]')))
            except Exception as e:
                pass
            if element != None:
                return {"status":"RESTRICTED", "content": list_content}
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "list-search")))
            try:
                list_search_result = element.find_elements_by_class_name("item")
                for element in list_search_result:
                    text = element.text
                    if len(text.split("\n")) >= 1:
                        name = text.split("\n")[0].strip()
                        description = ""
                        try:
                            description = text.split("\n")[1].strip()
                        except:
                            pass
                        
                        link = element.find_element_by_partial_link_text(name).get_attribute('href')
                        total_links.add(link)
                        nome_sem_acento = remove_caracter.removerAcentosECaracteresEspeciais(name)
                        resultado = compara_nome(nomecombinacao=name_without_accent, nomeperfil=nome_sem_acento, nomealuno=whole_name_accent, sex=sex)

                        if resultado:
                            
                            if description != "":
                            
                                list_content.append( {"name": name, "description": description, "link": link} )
                quantity_found = len(total_links)				
            except:
                print("\nERRO")
                pass
            time.sleep(30)
            list_pagination = driver.find_elements_by_class_name("page-item")
            cont_page -= 1
            if list_pagination != [] and cont_page > 1:
                list_pagination[-1].click()
            else:
                continuar = False
        return {"status":"SUCCESS", "content":list_content, "quantity_found":quantity_found}
    except:
        print("\nescavador_profile.f_get_link: Erro.\n")
        logging.exception("\nescavador_profile.f_get_link: {}\n".format( sys.exc_info() ) )
        return {"status":"ERROR", "content":list_content, "quantity_found":quantity_found}



def f_get_text(driver=None, url_profile=None):
    html_content = ""
    try:
        driver.get(url_profile)
        print("\n\n>>> Página Acessada: ", driver.title)
        print(">>> URL Acessada: ", driver.current_url)        
        element = None
        try:
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="escavador-app"]/div[1]/p[1]')))
        except Exception as e:
            pass
        if element != None:
            return {"status":"RESTRICTED", "content": {"url": url_profile, "date": str(date.today()), "html_content": html_content} }
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'html')))
        html_content = element.get_attribute('outerHTML')
        time.sleep(30)
        return {"status":"SUCCESS", "content":{"url": url_profile, "date": str(date.today()), "html_content": html_content}}
    except:
        print("\nescavador_profile.f_get_text: Erro.\n")
        logging.exception("\escavador_profile.f_get_text: {}\n".format( sys.exc_info() ) )
        return {"status":"ERROR", "content":{"url": url_profile, "date": str(date.today()), "html_content": html_content}}



def compara_nome(nomecombinacao=None, nomeperfil=None, nomealuno=None, sex=None):
    aux = nomeperfil.replace(".","")
    nomeperfil = aux.lower()
    aux = nomecombinacao.lower().replace(".","")
    nomecombinacao = aux
    lst_nomecombinacao = nomecombinacao.split(" ")
    lst_nomeperfil = nomeperfil.split(" ")
    nomealuno = nomealuno.lower()
    eh_mulher = True if sex in ["F","f"] else False
    if(nomecombinacao in nomeperfil) and (lst_nomecombinacao[0] == lst_nomeperfil[0] ):
        diferenca = len(lst_nomeperfil) - len(lst_nomecombinacao)
        if diferenca == 0:
            return True
        elif(eh_mulher):
            return True
        else:
            return False
          