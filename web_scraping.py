from webdriver import webdriver
from escavador_scraper import escavador_profile
from persistent_storage import crud
from datetime import date
import traceback
import logging
import logging.config
import backup
import time
import random
import shutil


# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "Erro: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."


def f_web_scraping_login():
    msg_user = '''\n
    ------------------------------------------------
     O navegador abriu para que seja feito o login!
     Para prosseguir responda a confirmação a seguir.
    ------------------------------------------------
    '''
    print(msg_user)
    try:
        # remove
        shutil.rmtree('./browser_cache')
    except:
        pass
    driver = webdriver.f_open_browser()
    driver.get("https://www.escavador.com/login")
    print()
    result = input("Fez login? (S/N): ")
    while result.strip().lower() != "s" and result.strip().lower() !="n" :
        result = input("Fez login? (S/N): ")   
    webdriver.f_close_browser(driver=driver)
    return result.strip().lower()
        
        
        
def f_web_scraping(search_today=10, find_today=10):
    
    driver = webdriver.f_open_browser()
    is_scrapered = False
    waiting_time_between_pages = 65
    waiting_time_between_combination = 300

    try:
        
        print("\n\nPROGRAMA INICIOU\n\n")
        # pega combinacoes de nomes do BD
        list_combinacao = crud.f_get_combinacao(is_scrapered= is_scrapered)
        
        msg = "Não há combinação de nome ou todas já foram pesquisadas!" if list_combinacao == [] else "Há "+str(len(list_combinacao))+" combinação de nome para pesquisar!"
        print(msg)
        
        # pega registros de páginas raspados na data atual
        list_escavador_found_today = crud.f_get_escavador(date= str(date.today()))
        
        while list_combinacao != [] and search_today > 0 and len(list_escavador_found_today) <= find_today:
            
            ##
            ## PRIMEIRA PARTE: SCRAPER LINKS
            ##
            
            # pega combinacao de nome da lista
            combinacao = list_combinacao[0]
            print("\nID COMBINACAO: {} | NOME COMBINACAO: {}\n".format(combinacao['id'],combinacao['name']))
            lst_aluno = crud.f_get_aluno(id= combinacao['aluno_id'])
            aluno = lst_aluno[0]
                
            print("\nScraper Links: INICIOU\n")
            # abre navegador
            list_link = None
            quantity_found = 0
            try:
                ### Recupera Backup
                result = backup.f_restaura()
                list_link_backup = result["list_link"]
                combinacao_backup = result["combinacao"]
                quantity_found = result["quantity_found"]
                if combinacao['id'] == combinacao_backup['id']:
                    list_link = list_link_backup if list_link_backup != None else []
            except:
                # pega os links dos perfis
                content = escavador_profile.f_get_link(driver= driver, name_person= combinacao['name'], whole_name=aluno["name"], sex=aluno["sex"])
                if content['status'] == "RESTRICTED" or content['status'] == "ERROR":
                    raise Exception ("Escavador Get Link: {}".format(content['status']))
                list_link = content['content']
                quantity_found = content['quantity_found']
            
            print("\nScraper Links: CONCLUIU\n")
            print("\nPerfis Encontrados: ", quantity_found)
            print("\nPerfis Selecionados: ", len(list_link))
            ### Salva Backup
            backup.f_salva(combinacao= combinacao, list_link= list_link,quantity_found= quantity_found)
            # fecha navegador
            webdriver.f_close_browser(driver=driver)
            
            
            ##
            ## SEGUNDA PARTE: SCRAPER PERFIS
            ##
            print("\nScraper Perfis: INICIOU\n")        
            # pega os dados da pagina
            while list_link != []:
                                
                # pega o link do perfil
                content_link = list_link[0]
                content = None
                # verifica se o perfil ja esta no BD
                list_escavador = crud.f_get_escavador(profile_url= content_link['link'])
                escavador_id = None
                if list_escavador != []:
                    escavador = list_escavador[0]
                    escavador_id = escavador["id"]
                else:
                    # abre navegador
                    driver = webdriver.f_open_browser()                
                    content = escavador_profile.f_get_text(driver= driver, url_profile= content_link['link'])
                    if content['status'] == "RESTRICTED" or content['status'] == "ERROR":
                        raise Exception ("Escavador Get Text: {}".format(content['status']) )
                    escavador = content['content']
                    # salva escavador
                    escavador_id = crud.f_save_escavador(combinacao_id=combinacao['id'], aluno_id=None,profile_name=content_link['name'],  profile_url= escavador['url'], date= escavador['date'], profile_page= escavador['html_content'])
                    # fecha navegador
                    webdriver.f_close_browser(driver=driver)
                    # tempo de espera entre cada página
                    time.sleep(waiting_time_between_pages)

                # apaga link de list_link
                del list_link[0]
                ### Atualiza Backup
                backup.f_salva(combinacao= combinacao, list_link= list_link,quantity_found= quantity_found)
            
            # atualiza combinacao
            crud.f_update_combinacao(id= combinacao['id'], aluno_id= combinacao['aluno_id'], name= combinacao['name'], is_scrapered= True, quantity_found= quantity_found)
            ### Apaga Backup
            backup.f_remove()
            print("\nScraper Perfis: CONCLUIU\n")
            # pega as combinacoes de nomes
            list_combinacao = crud.f_get_combinacao(is_scrapered= is_scrapered)
            # espera o tempo entre cada combinacao
            time.sleep( waiting_time_between_combination )

            search_today -= 1
            list_escavador_found_today = crud.f_get_escavador(date= str(date.today()))

    except:
        print(msg_error.format("função f_web_scraping", "não foi continuar a raspagem"))
        logger.info( traceback.format_exc() )
    finally:
        print("\n\n\nPROGRAMA TERMINOU \n\n\n")
        #fecha navegador
        webdriver.f_close_browser(driver=driver)