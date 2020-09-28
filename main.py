# coding: utf-8
'''
Programa principal que chama as funcionalidades do programa.
Deve ser executador por linha de comando passando um argumento: 

main.py <argumento>

    app_bd_create             Cria as tabelas do banco de dados 
    app_bd_drop               Apaga as tabelas do banco de dados
    app_loading_initial       Carrega os dados da planilha
    app_web_scraping          Inicia a coleta de dados dos egressos
    app_attach_label          Anexa rótulos nos dados coletados
    help                      Ajuda     
'''
import sys
import persistent_storage.model as model
import loading_initial
import web_scraping
import attach_label
import logging
import logging.config
import sys
import input_timeout
import traceback


# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger("main")
msg_error = "Erro: main.py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."


def f_confirmation():
    confirmation = input("Tem certeza que deseja prosseguir? (S/N) ")
    if confirmation.strip().lower() == "s":
        return True
    return False

def f_main(args):
    '''
    Função principal.
    
    Parâmetro
    ----------
        args (list<str>):
            args[1] que define a funcionalidade a ser executada pelo programa.
    
    Retorno
    ----------
        nulo
    '''
    
    help = '''
    app_bd_create             Cria as tabelas do banco de dados 
    app_bd_drop               Apaga as tabelas do banco de dados
    app_loading_initial       Carrega os dados da planilha
    app_web_scraping          Inicia a coleta de dados dos egressos
    app_attach_label          Anexa rótulos nos dados coletados
    help                      Ajuda                                          
    '''

    parameter_error =  False
    try:
        if len(args) != 2:
            parameter_error = True
        if args[1] == "app_bd_create":
            print("Cria Tabelas")
            if f_confirmation():
                result = model.f_create_tables(if_not_exists=True)
                print("Concluído" if not result else "Interrompido")
        elif args[1] == "app_bd_drop":
            print("Apaga tabelas")
            if f_confirmation():           
                result = model.f_drop_tables(if_exists=True)
                print("Concluído" if not result else "Interrompido")
        elif args[1] == "app_loading_initial":
            print("Carrega os dados da planilha")
            loading_initial.f_loading_initial()            
        elif args[1] == "app_web_scraping":
            print("\nInicia a coleta de dados dos egressos")
            search_today, find_today = None, None
            try:
                result = input_timeout.get_answer(msg="\n(10 segundos) Pesquisar hoje = ")
                search_today = 10 if result == None else int(result)
                result = input_timeout.get_answer(msg="\n(10 segundos) Coletar hoje = ")
                find_today = 10 if result == None else int(result)
            except:
                print(msg_error.format("função f_main", "Argumento search_today e find_today não identificados"))
                raise
            print("\nPesquisar hoje: {} e Coletar hoje: {}".format(search_today, find_today) )
            web_scraping.f_web_scraping(search_today=search_today, find_today=find_today)
            
        elif args[1] == "app_attach_label":
            print("Anexa rótulos nos dados coletados")
            attach_label.f_attach_label()
        elif args[1] == "help":
            print(help)
        else:
            parameter_error = True
            
    except:
        logger.error( traceback.format_exc() )
    finally:
        if parameter_error:
            print(msg_error.format("função f_main", "Argumento não identificado"))
            print(help)
        else:
            print(msg_error.format("função f_main", "O programa foi interrompido"))

    return None

if __name__ == "__main__":
    f_main(sys.argv)
