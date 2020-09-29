from persistent_storage import crud
import open_file_gui
import traceback
import logging
import logging.config
import estrutura_linkedin
import define_alumni

# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "Erro: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."

def f_remove_label():
    pass

def f_attach_label():
    
    # pega informações da planilha com dados nome da instituição, grau do curso e nome do curso
    list_institution_name = []
    list_formation = []
    list_study_area = []    
    try:
        file_name = open_file_gui.f_get_path()
        lista = open_file_gui.f_open_file(file_name)
        for line in lista:
            institution, formation, study_area = open_file_gui.f_line_split(line, 2)
            if institution.strip() != "": 
                list_institution_name.append( institution.strip() )
            if formation.strip() != "": 
                list_formation.append( formation.strip() )
            if study_area.strip() != "":
                list_study_area.append( study_area.strip() )           
    except:
        print(msg_error.format("função f_attach_label", "esperava uma planilha csv com as colunas (sem cabeçalho): 'nome da instituição | grau do curso |  nome do curso'"))
        logger.error("Esperva uma planilha csv com colunas: nome da instituição | grau do curso |  nome do curso " +  traceback.format_exc() )
        raise
                                          
    try:

        print("\nPROGRAMA INICIOU\n\n")
        
        print("Procura por:\n{}\n{}\n{}\n".format(list_institution_name, list_formation, list_study_area) )
        
        # pega combinacoes de nomes do BD
        linkedin_list = crud.f_get_linkedin(profile_json= None)
        
        msg = "Não há registros ou todos registros já foram processados!" if linkedin_list == [] else "Há "+str(len(linkedin_list))+" registros para processar!"
        print(msg)
        
        while linkedin_list != []:
            
            # pega combinacao de nome da lista
            period_start=""
            
            linkedin = linkedin_list[0]
            
            html_text = linkedin["profile_page"]
        
            htmlsoup = estrutura_linkedin.f_create_htmlsoup_from_text(html_text= html_text)
            linkedin["profile_json"] = estrutura_linkedin.f_create_json_from_html(html_soup= htmlsoup)
            
            combinacao_list = crud.f_get_combinacao(id= linkedin["combinacao_id"])
            
            combinacao = combinacao_list[0]
            
            aluno_list = crud.f_get_aluno(id= combinacao["aluno_id"])
            
            aluno = aluno_list[0]
            
            period_start = aluno["year_start"] if aluno["year_start"] != None else ""

            print("\nID LinkedIn: {}\nURL:{}\nAluno Nome: {}\nAno Inicio: {}\n".format(linkedin["id"], linkedin["profile_url"],aluno["name"], aluno["year_start"]) )
            
            is_alumni = define_alumni.f_define_alumni(json_profile= linkedin["profile_json"],
                                                    institution_name= list_institution_name,
                                                    formation= list_formation,
                                                    study_area= list_study_area,
                                                    period_start= period_start)
            aluno_id = combinacao["aluno_id"] if is_alumni else None
            
            lst_escavador = crud.f_update_linkedin(id=linkedin["id"],
                                                profile_url=linkedin["profile_url"],
                                                aluno_id= aluno_id,
                                                date= linkedin["date"],
                                                profile_page= linkedin["profile_page"],
                                                profile_json= linkedin["profile_json"])

            linkedin_list = crud.f_get_linkedin(profile_json= None)
    except:
        print(msg_error.format("função f_attach_label", "Algo errado aconteceu"))
        logger.error( traceback.format_exc() )
    finally:
        print("\n\nPROGRAMA TERMINOU \n\n\n")
