# coding: utf-8

import sys
import persistent_storage.model as model
import loading_initial
import web_scraping
import attach_label
import logging
import logging.config
import sys
import traceback


# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger("main")
msg_error = "\nErro: main.py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."


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
    Comando esperado: python3 main.py <argumento>
    
    ----------------------------------------------------------------------------
    Argumento básico
    ----------------------------------------------------------------------------
    cria_base                         Cria banco de dados
    apaga_base                        Apaga banco de dados
    carrega_planilha                  Carrega os dados da planilha sem cabeçalho,
                                      ou seja, armazena a primeira linha
    coleta_dados                      Inicia a coleta de dados dos egressos
    marca_dados                       Anexa rótulos nos dados coletados
    ajuda                             Mensagem de ajuda                
    
    ----------------------------------------------------------------------------
    Argumento composto
    ----------------------------------------------------------------------------
    carrega_planilha com_cabecalho    Carrega os dados da planilha com cabeçalho,
                                      ou seja, ignora a primeira linha
    coleta_dados login                Abre navegador na página de login
    marca_dados desfazer              Apaga rótulos nos dados coletados
                          
    '''

    parameter_error =  False
    try:
        if len(args) < 2 or len(args) > 3:
            parameter_error = True
            raise ValueError("Quantidade de argumentos inválido!")
        elif args[1] == "cria_base":
            print("Cria base")
            if f_confirmation():
                result = model.f_create_tables(if_not_exists=True)
                print("Concluído" if not result else "Interrompido")
        elif args[1] == "apaga_base":
            print("Apaga tabelas")
            if f_confirmation():                         
                result = model.f_drop_tables(if_exists=True)
                print("Concluído" if not result else "Interrompido")
        elif args[1] == "carrega_planilha":
            print("Carrega os dados da planilha")
            if len(args) == 2:
                result = loading_initial.f_loading_initial()
                print("Concluído" if result else "Interrompido")                
            elif len(args) == 3 and args[2] == "com_cabecalho": 
                result = loading_initial.f_loading_initial(with_header=True)
                print("Concluído" if result else "Interrompido")
            else:
                parameter_error = True  
        elif args[1] == "coleta_dados":
            print("\nColeta de dados dos egressos")
            if len(args) == 2:
                web_scraping.f_web_scraping()
            elif len(args) == 3 and args[2] == "login": 
                result = web_scraping.f_web_scraping_login()
                if result == "s":
                    web_scraping.f_web_scraping()
            else:
                parameter_error = True  
        elif args[1] == "marca_dados":
            print("Rotula dados coletados", end="")
            if len(args) == 2:
                print()
                attach_label.f_attach_label()
            elif len(args) == 3 and args[2] == "desfazer":
                print(" desfazer")
                if f_confirmation():   
                    attach_label.f_remove_label()
            else:
                parameter_error = True             
        elif args[1] == "ajuda":
            print(help)
        else:
            parameter_error = True
            
    except:
        logger.error( traceback.format_exc() )
        if not parameter_error:
            print(msg_error.format("função f_main", "O programa foi interrompido"))

    finally:
        if parameter_error:
            print(msg_error.format("função f_main", "Argumento não identificado"))
            print(help)

    return None

if __name__ == "__main__":
    f_main(sys.argv)
