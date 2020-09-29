from tkinter import Tk
from tkinter.filedialog import askopenfilename
import chardet


def f_line_split(line, delimitator_quantity ):
    if line.count(",") == delimitator_quantity:
        return tuple( line.strip().split(",") )
    elif line.count(";") == delimitator_quantity:
        return tuple( line.strip().split(";") )
    msg = "Arquivo planilha csv tem número de colunas inválido! O esperado é "+ str(delimitator_quantity + 1)+" colunas com um delimitador ',' ou ';'. "
    raise Exception (msg)

def f_get_path():
    # seleciona arquivo
    Tk().withdraw()
    file_name = askopenfilename()
    if "csv" in file_name.lower():
        return file_name
    raise ValueError("Arquivo não é uma planilha csv")
    return ""

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