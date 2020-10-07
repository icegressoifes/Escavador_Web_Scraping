import chardet
import logging
import logging.config
import json
import traceback


# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "Erro: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."



def f_line_split(line, delimitator_quantity ):
    if line.count(",") == delimitator_quantity:
        return tuple( line.strip().split(",") )
    elif line.count(";") == delimitator_quantity:
        return tuple( line.strip().split(";") )
    msg = "Arquivo planilha csv tem número de colunas inválido! O esperado é "+ str(delimitator_quantity + 1)+" colunas com um delimitador ',' ou ';'. "
    raise Exception (msg)

def f_get_path():
    dic_configuration_full = {}
    dir_planilha = ""

    try:
        with open("configuracao.json", "r") as json_file:
            dic_configuration_full = json.load(json_file)
  
        dir_planilha = dic_configuration_full["dir_planilha"]
        if dir_planilha == "":
            print(msg_error.format("função f_get_path", "o arquivo 'condiguracao.json' não contém o diretório da planilha"))
            raise Exception ("o arquivo 'condiguracao.json' não contém o diretório da planilha")        
    except:
        print(msg_error.format("função f_get_path", "Não foi possível ler os dados do arquivo 'configuracao.json'"))
        logger.info( traceback.format_exc() )
        raise
     
    return dir_planilha

def f_open_file(file_name):
    # tratamento do caminho do arquivo
    file_path = file_name.replace("/", "//")
    # verifica o enconding do arquivo
    obj_file = open(file_path, 'rb').read()
    result = chardet.detect(obj_file)
    # abre o arquivo com a codificação correta e cria a listas
    obj_file = open(file_path, "r", encoding=result['encoding'])
    lista =  obj_file.readlines()
    obj_file.close()
    return lista