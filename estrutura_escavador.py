# coding:utf-8
from bs4 import BeautifulSoup
import json
import re
import logging
import logging.config
import traceback
import sys


# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "Aviso: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."


def f_create_htmlsoup_from_file(name_file=None):
    with open(file=name_file, mode="r") as file:
        return BeautifulSoup(file,'html.parser')

def f_create_htmlsoup_from_text(html_text=None):
    return BeautifulSoup(html_text, 'html.parser')

def f_create_json_from_html(html_soup=None):

    name, localization, about = f_get_overview(html_soup)    
    experience_list = f_get_experience_list(html_soup)
    education_list = f_get_education_list(html_soup)
    dic_profile = {}  
    dic_profile["nome"] = f_prepare_text( name )
    dic_profile["sobre"] = f_prepare_text( about )
    dic_profile["localizacao"] = f_prepare_text( localization )
    dic_profile["academico"] = education_list
    dic_profile["profissional"] = experience_list
    
    json_dicprofile = json.dumps(dic_profile, ensure_ascii=False)

    return json_dicprofile


# get overview
def f_get_overview(html_soup=None):
    # get name
    name = ""
    try:
        h1_element = html_soup.select_one('#usuario > div.container.-rel > div > header > div > div.body > h1')
        name = h1_element.get_text()
    except:
        print(msg_error.format("função f_get_overview", "o nome do perfil não coletado"))
        logger.error( traceback.format_exc() )
   
    
    # get localization
    localization = ""
    try:
        div_element = html_soup.find(id="endereco-profissional")
        ul_element = div_element.find("ul",class_="list-block")
        text = ul_element.get_text()
        localization = f_prepare_text( text.strip() )
    except:
        print(msg_error.format("função f_get_overview", "o endereço profissional não foi coletado"))
        logger.error( traceback.format_exc() )
                
    # get about
    about = ""
    try:
        div_element =  html_soup.select_one('#usuario > div.container.-rel > div > header > div > div.box.-flushHorizontal')
        about = div_element.get_text()
    except:
        print(msg_error.format("função f_get_overview", "o resumo geral não foi coletado"))
        logger.error( traceback.format_exc() )          
        
    return (name, localization, about)   


# get education
def f_get_education_list(html_soup=None):
    lst_dic_curso = []
    try:
      academico =  html_soup.select_one('#formacao > div > div.list-inline.inline-edit-content.row')
      lst_curso = academico.find_all('div')
   
      for curso in lst_curso:
          
          titulo_curso = ""
          ano_inicio = ""
          ano_fim = ""
          nome_instituicao = ""
          titulo_trabalho = ""
          
          try:
            titulo_curso = curso.find('p', class_="heading -likeH5 inline-edit-item inline-edit-item-formacao").get_text()
            intervalo_ano = curso.find(class_='heading -likeH5 inline-edit-item').get_text()
            ano_inicio = intervalo_ano.split("-")[0].strip()
            ano_fim = intervalo_ano.split("-")[1].strip()
            nome_instituicao = curso.find(class_="inline-edit-item-instituicao-nome").get('value')
            titulo_trabalho = None
            try:
                a = curso.get_text()  
                for linha in a.split("\n"):
                    if "titulo" in linha.lower() or "título" in linha.lower():
                        titulo_trabalho = ' '.join( linha.split(" ")[1:] )
            except:
                pass
            lst_dic_curso.append({"curso": f_prepare_text( titulo_curso ),
                                  "instituicao": f_prepare_text( nome_instituicao ),
                                  "titulo": f_prepare_text( titulo_curso ),
                                  "ano_inicio": ano_inicio,
                                  "ano_fim": ano_fim })    
          except:
            pass
    except:
      print(msg_error.format("função f_get_education_list", "algumas informações acadêmica não foram coletadas"))
      logger.error( traceback.format_exc() ) 
    
    return lst_dic_curso



# get experience
def f_get_experience_list(html_soup=None):
    lst_dic_profissao = []
    try:
      profissional_content  = html_soup.select_one('#atuacao-profissional')
      lst_profissao = profissional_content.find_all('div', class_="col-sm-6 inline-edit-item-box clearfix-box")
      for p in lst_profissao:
          descricao = ""
          ano_inicio = None
          ano_fim = None
          nome_instituicao = ""
          vinculo = ""
          enquadramento_funcional = ""
          carga_horaria = None
          atividade = ""
          try:
              descricao = p.find(class_="inline-edit-item-descricao")
              paragrafo_descricao = descricao.find('p').get_text()
              intervalo_ano = p.find(class_='heading -likeH5 inline-edit-item').get_text()
              ano_inicio = intervalo_ano.split("-")[0].strip()
              ano_fim = intervalo_ano.split("-")[1].strip()
              nome_instituicao = p.find(class_="inline-edit-item-instituicao-nome").get('value')
              for parte in paragrafo_descricao.split(","):
                    
                    if "Vínculo" in parte:
                        vinculo = parte.split("Vínculo:")[1].strip()
                    if "Enquadramento Funcional" in parte:
                        enquadramento_funcional = parte.split("Enquadramento Funcional:")[1].strip()
                    if "Carga horária" in parte: 
                        carga_horaria = parte.split("Carga horária: ")[1].strip()
                        
              try:
                atividade = p.find(class_="atividades").get_text()
              except:
                pass
          except:
            pass          
          
          lst_dic_profissao.append({"vinculo":f_prepare_text( vinculo ),
                                    "enquadramento_funcional": f_prepare_text( enquadramento_funcional ),
                                    "carga_horaria":carga_horaria ,
                                    "organizacao":f_prepare_text( nome_instituicao),
                                    "ano_inicio":ano_inicio,
                                    "ano_fim":ano_fim,
                                    "atividade":f_prepare_text( atividade ) })

    except:
      print(msg_error.format("função f_get_experience_list", "algumas informações profissional não foram coletadas"))
      logger.error( traceback.format_exc() ) 
                
    return lst_dic_profissao
    
    
def f_prepare_text( text ):
  new_text = text
  try:
    aux = ""
    for line in text.split("\n"):
      if line != "" and "\n":
        aux += line.strip() + "\n"
    aux = aux.strip()  
    new_text = aux.replace('"', '')
    aux = new_text
    new_text = aux.replace("'", "")
    aux = new_text    
    new_text = aux.replace('\r\n', '\\n')
    aux = new_text
    new_text = aux.replace('\n', '\\n')
  except:
    logging.exception("f_prepare_text error: {}".format( sys.exc_info() ) )    
    pass
  return new_text


  