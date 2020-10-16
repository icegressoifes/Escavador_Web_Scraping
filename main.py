# coding: utf-8

import sys
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
    Comando esperado: main.py <argumento>
    
    ----------------------------------------------------------------------------
    Argumentos
    ----------------------------------------------------------------------------
    carrega_planilha                     Carrega os dados da planilha csv
    coleta_dados                         Inicia a coleta de dados dos egressos
    coleta_dados login <user> <pass>     Faz autenticação no site
    coleta_dados logout                  Remove autenticação no site
    marca_dados                          Anexa rótulos nos dados coletados   
    marca_dados desfazer                 Apaga rótulos nos dados coletados
    ajuda                                Mensagem de ajuda                
                          
    '''

    parameter_error =  False
    try:

        if len(args)>1 and args[1] == "carrega_planilha":
            print("Carrega os dados da planilha")
            result = loading_initial.f_loading_initial(with_header=True)
            print("Concluído" if result else "Interrompido")
        elif len(args)>1 and args[1] == "coleta_dados":
            print("\nColeta de dados dos egressos", end=" ")
            if len(args) == 2:
                web_scraping.f_web_scraping()
            elif len(args) == 5 and args[2] == "login": 
                print("entrar")
                result = web_scraping.f_web_scraping_login(user=args[3], password=args[4])
                if result == "s":
                    web_scraping.f_web_scraping()
            elif len(args) == 3 and args[2] == "logout": 
                print("sair")
                result = web_scraping.f_web_scraping_logout()
                if result == "s":
                    web_scraping.f_web_scraping()
            else:
                parameter_error = True 
            print()
        elif len(args)>1 and args[1] == "marca_dados":
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
        elif len(args)>1 and args[1] == "ajuda":
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
