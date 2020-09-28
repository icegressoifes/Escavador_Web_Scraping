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


def f_check_login(driver=None):
	# url = "https://www.linkedin.com/feed/"
	# driver.get( url )
	# time.sleep(5)
	# if driver.current_url in url:
	# 	return True
	# return False
	pass



def f_login(driver=None, user=None, password=None, remember=True):
	# driver.get("https://www.linkedin.com/uas/login?session_redirect=%2Fvoyager%2FloginRedirect%2Ehtml&amp;fromSignIn=true&amp;trk=uno-reg-join-sign-in")
	# try:
	# 	# time.sleep(30)
	# 	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
	# 	rememberme_checkbox = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/label')
	# 	input_user = driver.find_element_by_name('session_key')
	# 	input_password = driver.find_element_by_name('session_password')
	# 	button_submit = driver.find_element_by_tag_name('button')

	# 	# cadeia de ações
	# 	actions = ActionChains(driver)
	# 	actions.pause( 4 )
	# 	actions.move_to_element(input_user)
	# 	actions.double_click(input_user)
	# 	actions.pause(3)
	# 	actions.send_keys(user)
	# 	actions.pause(6)
	# 	actions.move_to_element(input_password)
	# 	actions.double_click(input_password)
	# 	actions.pause(6)
	# 	actions.send_keys(password)
	# 	actions.pause(4)
	# 	if remember:
	# 		actions.move_to_element(rememberme_checkbox)
	# 		actions.click(rememberme_checkbox)
	# 		actions.pause( 2 )
	# 	actions.move_to_element(button_submit)
	# 	actions.click(button_submit)
	# 	actions.perform()
	# except:
	# 	print("\nlinkedin_profile.f_login: Falha a realizar login!\n")

	# finally:
	# 	driver.get("https://www.linkedin.com/feed")
	# 	time.sleep(20)
	# 	pass
	pass



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
								print(description)
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
		  