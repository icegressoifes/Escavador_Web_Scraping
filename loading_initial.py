from escavador_scraper import generate_combination_name
from persistent_storage import crud
from escavador_scraper import open_file_gui
import logging
import logging.config
import traceback


# Definicao de log
logging.config.fileConfig('logconf.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
msg_error = "Erro: "+__name__+".py - {}: {}. Para mais detalhes verifique o arquivo 'error.log'."


def f_loading_initial(with_header=False):
    file_name = open_file_gui.f_get_path()
    lista = open_file_gui.f_open_file(file_name)
    index_initial = 1 if with_header else 0
    for linha in lista[index_initial: ]:
        nome, data, sexo, ano_inicio, ano_fim = None, None, None, None, None
        try:
            coluna = open_file_gui.f_line_split(linha, 8)
        except:
            print(msg_error.format("função f_loading_initial", "esperava uma planilha csv com as colunas: 'matricula | nome aluno | data nasc. | nome curso | ano inicial | periodo inicial | ano final | periodo final | sexo'"))
            logger.error("Esperva uma planilha csv com colunas: matricula | nome aluno | data nasc. | nome curso | ano inicial | periodo inicial | ano final | periodo final | sexo " +  traceback.format_exc())   
            raise           
        
        nome = coluna[1]
        try:
            if len(coluna[2][6:]) == 4 and len(coluna[2][3:5]) == 2 and len(coluna[2][0:2]) == 2:
                data = "{}-{}-{}".format(coluna[2][6:], coluna[2][3:5], coluna[2][0:2])
            elif coluna[2] != "":
                raise ValueError ("Era esperado a data no formato 'DD-MM-AAAA' ou então vazio ''")
        except ValueError as ve:
            print(msg_error.format("função f_loading_initial ", ve))
            logger.error(msg_error.format("função f_loading_initial ", ve))
            raise  
                
        sexo = coluna[8]
        ano_inicio = coluna[4] if coluna[4] != "" else None
        ano_fim = coluna[6] if coluna[6] != "" else None
        lista_combinacao = generate_combination_name.f_combination_name(nome)
        id_aluno = crud.f_save_aluno(name=nome, sex=sexo, birth_date=data, year_start= ano_inicio, year_end= ano_fim)
        if id_aluno:
            for nome_combinacao in lista_combinacao:
                crud.f_save_combinacao(aluno_id=id_aluno, name=nome_combinacao, is_scrapered=False)
                
    return True

	
if __name__ == '__main__':
    print("Função f_loading_database")