def f_remove_stopword( string ):
	stopword = ["da", "de", "do", "dos","das"]
	nova_string = ""
	for parte in string.split():
		if (parte.lower() not in stopword):
			nova_string += parte + " "
	return nova_string.strip()


def f_mapea_stopwords_words(nome):
	uniao = ""
	dic = {}
	for palavra in nome.split():
		if uniao != "":
			dic[palavra] = uniao + " " + palavra
			uniao = ""
		if palavra.lower() in ["da", "de", "do", "dos","das"]:
			uniao = palavra
	return dic

def f_combination_name(nome):
	setNome = set([])
	# remove stopWords
	novoNome = f_remove_stopword( nome )
	# nome completo
	if(len(novoNome.split())  > 1):
		setNome.add( novoNome )
	# nome formado pelo primeiro nome e um dos sobrenomes
	if(len(novoNome.split())  > 2):
		for i in range(1, len(novoNome.split()) ):
			resultado = "{} {}".format(novoNome.split()[0], novoNome.split()[i])
			setNome.add( resultado )
	# nome formado pelo primeiro nome e alguns dos sobrenomes
	if(  len(novoNome.split()) > 2):
		for i in range(1, len(novoNome.split()) ):
			resultado = novoNome.split()[0]
			for j in range (1, len(novoNome.split()) ):
				if (i != j):
					resultado += " " + novoNome.split()[j]
			setNome.add( resultado )
    # abrevia nomes combinados
	setAbreviado = set([])	
	for nomeCombinado in setNome:
		if(len(nomeCombinado.split() ) > 2):
			# abrevia um dos nomes
			for i in range(1, len(nomeCombinado.split())-1):
				nomeAbreviado = nomeCombinado.split()[0]
				for j in range(1, len(nomeCombinado.split())-1):
					if(i == j):
						nomeAbreviado = nomeAbreviado + " " + nomeCombinado.split()[j][0]
					else:
						nomeAbreviado = nomeAbreviado + " " + nomeCombinado.split()[j]
				nomeAbreviado = nomeAbreviado + " " + nomeCombinado.split()[-1]
				setAbreviado.add(nomeAbreviado)
			# abrevia todos os nomes internos
			nomeAbreviado = nomeCombinado.split()[0]
			for n in nomeCombinado.split()[1:-1]:
				nomeAbreviado = nomeAbreviado + " " + n[0]
			nomeAbreviado = nomeAbreviado + " " + nomeCombinado.split()[-1]
			setAbreviado.add(nomeAbreviado)
	if (len(setAbreviado) > 0):
		setNome.update( list(setAbreviado) )

	# adiciona os stopwords
	dic = f_mapea_stopwords_words( nome )
	setAdicionaStopwords = set([])
	for nome_completo in setNome:
		novo_nome = nome_completo
		for parte in nome_completo.split():
			if parte in dic:
				novo_nome = novo_nome.replace(parte, dic[parte])
		setAdicionaStopwords.add(novo_nome)
	setNome.update( list(setAdicionaStopwords) )

	# converte conjuto para lista
	lista_nomes = list(setNome)


	# ordena do maior para o menor em ordem alfabética	
	if len(lista_nomes) >= 1:
		for i in range(1, len(lista_nomes)): 
			key = lista_nomes[i] 
			j = i-1
			while j >=0 and (len(key) < (len(lista_nomes[j]))) : 
					lista_nomes[j+1] = lista_nomes[j] 
					j -= 1
			lista_nomes[j+1] = key
	lista_nomes.reverse()
	return lista_nomes