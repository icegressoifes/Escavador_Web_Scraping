# coding:utf-8
from bs4 import BeautifulSoup
import json
import re
import logging
import sys

# Definicao de logfind_elements
logging.basicConfig(filename='error.log', filemode='w', level=logging.ERROR, format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


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

def f_get_format_date(text_date):
    period_list = ["", ""]
    dic_month = { "jan.": "1",
                "fev.": "2",
                "mar.": "3",
                "abr.": "4",
                "mai.": "5",
                "jun.": "6",
                "jul.": "7",
                "ago.": "8",
                "set.": "9",
                "out.": "10",
                "nov.": "11",
                "dez.": "12" }
    try:
        period_list[0] = text_date.split("–")[0].strip()
        period_list[1] = text_date.split("–")[1].strip()
        
        for i in range ( len(period_list) ):
            if ". " in period_list[i]:
                month = period_list[i].split(" ")[0]
                period_list[i] = period_list[i].replace( month, dic_month[month] )
                period_list[i] = period_list[i].split(" ")[0].zfill(2) + "/" + period_list[i].split(" ")[-1]
    except:
        logging.exception("f_get_format_date error: {}".format( sys.exc_info() ) )    
    return (period_list[0], period_list[1])



# get overview
def f_get_overview(html_soup=None):
    # get name
    name = ""
    try:
        ul_element_list = html_soup.find_all('ul', class_="pv-top-card--list")
        li_element_list = ul_element_list[0].find_all('li')
        text = li_element_list[0].get_text()
        name = text.strip()
    except:
        logging.exception("f_get_overview get name overview error: {}".format( sys.exc_info() ) )
   
    
    # get localization
    localization = ""
    try:
        ul_element_list = html_soup.find_all('ul', class_="pv-top-card--list")
        li_element_list = ul_element_list[1].find_all('li')
        text = li_element_list[0].get_text()
        localization = text.strip()
    except:
        logging.exception("f_get_overview get localization overview error: {}".format( sys.exc_info() ) )        
          
    # get about
    about = ""
    try:
        p_element = html_soup.find('p', class_="pv-about__summary-text")
        span_element_list = p_element.find_all('span')
        text = span_element_list[0].get_text()
        about = text.strip()
    except:
       logging.exception("f_get_overview get about overview error: {}".format( sys.exc_info() ) )         
        
    return (name, localization, about)   


# get education
def f_get_education_list(html_soup=None):
    education_list = []
    try:
        section_element = html_soup.find('section', class_="education-section")
        li_element_list = section_element.find_all('li', class_="pv-profile-section__card-item")
        for li_element in li_element_list:
            organization_name = ""
            formation = ""
            study_area = ""
            study_period = ""            

            # get organization name
            h3_element = li_element.find('h3', class_="pv-entity__school-name")
            text = h3_element.get_text()
            organization_name = text.strip()
            
            # get formation
            try:
                p_element = li_element.find('p', class_="pv-entity__degree-name")
                span_element = p_element.find('span', class_="pv-entity__comma-item")
                text = span_element.get_text()
                formation = text.strip()                
            except:
                formation = ""
                logging.exception("f_get_education_list get formation error: {}".format( sys.exc_info() ) ) 

            # get study area
            try:
                p_element = li_element.find('p', class_="pv-entity__fos")
                span_element = p_element.find('span', class_="pv-entity__comma-item")
                text = span_element.get_text()
                study_area = text.strip()    
            except:
                study_area = ""
                logging.exception("f_get_education_list get study area error: {}".format( sys.exc_info() ) )                 
            
        
            # get study period 
            try:
                p_element = li_element.find('p', class_="pv-entity__dates")
                span_element = p_element.find_all('span')
                text = span_element[1].get_text()
                study_period = text.strip()
            except:
                study_period = ""
                logging.exception("f_get_education_list get study period error: {}".format( sys.exc_info() ) )   
                
            
            period_start, period_end = f_get_format_date( study_period )
            
            education = { "curso": f_prepare_text( study_area ),
                          "instituicao": f_prepare_text( organization_name ),
                          "titulo": f_prepare_text( formation ), 
                          "ano_inicio": period_start,
                          "ano_fim": period_end }
            
            education_list.append(education)    

    except:
        logging.exception("f_get_education_list error: {}".format( sys.exc_info() ) ) 
    
    return education_list       



# get experience
def f_get_experience_list(html_soup=None):
    experience_list = []
    try:
        section_element_list = html_soup.find_all('section', class_="pv-profile-section__card-item-v2")
        for section_element in section_element_list:
            organization_name = ""
            job_period = ""
            locality = ""
            job = ""
            h3_element = section_element.find('h3')
            li_element_list = section_element.find_all('li', class_="pv-entity__position-group-role-item")
            if len(li_element_list) == 0: # single job in organization
       
                # get job
                text = h3_element.get_text()
                job = text.strip()
                
                # get name organization                    
                p_element = section_element.find('p', class_="pv-entity__secondary-title")
                text = p_element.get_text()
                text = text.strip()
                organization_name = text.split("\n")[0]
                
                # get period employment
                try:
                    h4_element = section_element.find('h4', class_="pv-entity__date-range")
                    span_element_list = h4_element.find_all('span')
                    text = span_element_list[1].get_text()
                    job_period = text.strip()
                except:
                    job_period = ""
                    logging.exception("f_get_experience_list get job_period error: {}".format( sys.exc_info() ) ) 

               
                # get locality
                try:
                    h4_element = section_element.find('h4', class_="pv-entity__location")
                    span_element_list = h4_element.find_all('span')
                    text = span_element_list[1].get_text()
                    locality = text.strip()
                except:
                    locality = ""
                    logging.exception("f_get_experience_list get locality experience error: {}".format( sys.exc_info() ) )                     

                    
                period_start, period_end = f_get_format_date( job_period )

                experience = { "vinculo":f_prepare_text( job ),
                               "organizacao":f_prepare_text( organization_name ),
                               "ano_inicio":period_start, "ano_fim":period_end,
                               "localizacao":f_prepare_text( locality ) }
                
                experience_list.append(experience)

            elif len(li_element_list) != 0: # several jobs in organization
              
                # get organization name
                span_element_list = h3_element.find_all('span')
                text = span_element_list[1].get_text()
                organization_name = text.strip()
                               
                for li_element in li_element_list:
                        
                    # get job
                    h3_element = li_element.find('h3', class_="t-14")
                    span_element_list = h3_element.find_all('span')
                    text = span_element_list[1].get_text()
                    job = text.strip()
                    
                    # get period employment
                    h4_element = li_element.find('h4', class_="pv-entity__date-range")
                    span_element_list = h4_element.find_all('span')
                    text = span_element_list[1].get_text()
                    job_period = text.strip()
                    
                    # get locality
                    try:
                        h4_element = li_element.find('h4', class_="pv-entity__location")
                        span_element_list = h4_element.find_all('span')
                        text = span_element_list[1].get_text()
                        locality = text.strip()
                    except:
                        locality = ""
                        logging.exception("f_get_experience_list get locality experience error: {}".format( sys.exc_info() ) )    
                        
                        
                    period_start, period_end = f_get_format_date( job_period )
                        
                    experience = { "vinculo":f_prepare_text( job ),
                                   "organizacao":f_prepare_text( organization_name ),
                                   "ano_inicio":period_start, "ano_fim":period_end,
                                   "localizacao":f_prepare_text( locality ) }
                
                    experience_list.append(experience) 
                                
                    job_period = ""
                    locality = ""
                    job = ""
                    
    except Exception as e:
        logging.exception("f_get_experience_list error: {}".format( sys.exc_info() ) )    
        print("f_get_experience_list error {}".format(e))

    return experience_list
    
    

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


  