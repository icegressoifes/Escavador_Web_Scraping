from persistent_storage import crud
import open_file_gui
import traceback
import logging
import logging.config
import estrutura_escavador
import define_alumni
import json

# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "Erro: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."

def f_remove_label():
    crud.f_escavador_remove_label()

def f_attach_label():
    
    list_search_data = None
    with open("config_marcacao.json", "r") as json_file:
        list_search_data = json.load(json_file)
  

    print("\nIdentificador das opções de pesquisa disponíveis: ")
    dic_option = {}
    for i in range ( len(list_search_data) ):
        print(" > ", list_search_data[i]["identificador"])
        dic_option[ list_search_data[i]["identificador"] ] = i
    print()   
    option_selected = input("Digite o identificador para continuar (ou deixe vazio para sair): ")
    while option_selected != "" and option_selected not in dic_option:
        option_selected = input("Digite o identificador para continuar (ou deixe vazio para sair): ")
    
    if option_selected != "":
        index = dic_option[option_selected]
        dic_search_data = list_search_data[index]
        list_institution_name = dic_search_data["nome_instituicao"]
        list_formation = dic_search_data["grau_academico"]
        list_study_area = dic_search_data["nome_curso"]

        # try:
        #     file_name = open_file_gui.f_get_path()
        #     lista = open_file_gui.f_open_file(file_name)
        #     for line in lista:
        #         institution, formation, study_area = open_file_gui.f_line_split(line, 2)
        #         if institution.strip() != "": 
        #            list_institution_name.append( institution.strip() )
        #         if formation.strip() != "": 
        #             list_formation.append( formation.strip() )
        #         if study_area.strip() != "":
        #             list_study_area.append( study_area.strip() )           
        # except:
        #     print(msg_error.format("função f_attach_label", "esperava uma planilha csv com as colunas (sem cabeçalho): 'nome da instituição | grau do curso |  nome do curso'"))
        #     logger.error("Esperva uma planilha csv com colunas: nome da instituição | grau do curso |  nome do curso " +  traceback.format_exc() )
        #     raise
                                            
        try:

            print("\nPROGRAMA INICIOU\n\n")
            
            print("Procura por:\n{}\n{}\n{}\n".format(list_institution_name, list_formation, list_study_area) )
            
            # pega combinacoes de nomes do BD
            escavador_list = crud.f_get_escavador(profile_json= None)
            
            msg = "Não há registros ou todos registros já foram processados!" if escavador_list == [] else "Há "+str(len(escavador_list))+" registros para processar!"
            print(msg)
            
            while escavador_list != []:
                
                # pega combinacao de nome da lista
                period_start=""
                
                escavador = escavador_list[0]
                
                html_text = escavador["profile_page"]
            
                htmlsoup = estrutura_escavador.f_create_htmlsoup_from_text(html_text= html_text)
                escavador["profile_json"] = estrutura_escavador.f_create_json_from_html(html_soup= htmlsoup)
                
                combinacao_list = crud.f_get_combinacao(id= escavador["combinacao_id"])
                
                combinacao = combinacao_list[0]
                
                aluno_list = crud.f_get_aluno(id= combinacao["aluno_id"])
                
                aluno = aluno_list[0]
                
                period_start = aluno["year_start"] if aluno["year_start"] != None else ""

                print("\nID Escavador: {}\nURL:{}\nAluno Nome: {}\nAno Inicio: {}\n".format(escavador["id"], escavador["profile_url"],aluno["name"], aluno["year_start"]) )
                
                is_alumni = define_alumni.f_define_alumni(json_profile= escavador["profile_json"],
                                                        institution_name= list_institution_name,
                                                        formation= list_formation,
                                                        study_area= list_study_area,
                                                        period_start= period_start)
                aluno_id = combinacao["aluno_id"] if is_alumni else None
                
                lst_escavador = crud.f_update_escavador(id= escavador["id"],
                                                    profile_url= escavador["profile_url"],
                                                    aluno_id= aluno_id,
                                                    date= escavador["date"],
                                                    profile_page= escavador["profile_page"],
                                                    profile_json= escavador["profile_json"])

                escavador_list = crud.f_get_escavador(profile_json= None)
        except:
            print(msg_error.format("função f_attach_label", "Algo errado aconteceu"))
            logger.error( traceback.format_exc() )
        finally:
            print("\n\nPROGRAMA TERMINOU \n\n\n")
