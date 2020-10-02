import pickle
import os
import logging
import sys



def f_salva(combinacao=None, list_link=None,quantity_found=None):
	try:
		dic = {
			"combinacao": combinacao,
			"list_link":list_link,
			"quantity_found":quantity_found
		}		
		arq_write = open("./backup.bin","wb")
		pickle.dump(dic, arq_write)
		arq_write.close()
		return True
	except:
		print("\nbackup.f_salva: Erro ao restaurar o arquivo de backup.\n")
		logging.exception("\nbackup.f_salva: {}\n".format( sys.exc_info() ) )
		return False




def f_restaura():
	try:
		if (os.path.exists("./backup.bin")):			
			arq_read = open("./backup.bin","rb")
			dic = pickle.load(arq_read)
			arq_read.close()
			return dic
	except:
		print("\nbackup.f_restaura: Erro ao restaurar o arquivo de backup. \n")
		logging.exception("\nbackup.f_restaura: {}\n".format( sys.exc_info() ) )
		return False




def f_remove():
	try:
		os.remove("./backup.bin")
		return True
	except:
		print("\nbackup.f_remove: Erro ao restaurar o arquivo de backup. \n")
		logging.exception("\nbackup.f_remove: {}\n".format( sys.exc_info() ) )
		return False