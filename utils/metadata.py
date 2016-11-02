# -*- coding: utf-8 -*-
from operator import itemgetter
KEYWORDS_PADRAO = [u'fotografia', u'eventos', u'ensaios', u'Anne Tozetto', u'Annelize Tozetto', u'fotografia ponta grossa', u' fotografia curitiba']
DESCRIPTION_PADRAO = u'Oi gente! Meu nome é Annelize e aqui é onde publico meus trabalhos da minha paixão: fotografia! Amo fotojornalismo, crianças, famílias e casais!'

PRONOMES = [u'eu', u'me', u'mim', u'comigo', u'nós', u'nos', u'conosco', u'tu', u'te', u'ti', u'contigo',
			u'vós', u'vos', u'convosco', u'se', u'si', u'consigo', u'ele', u'eles', u'o', u'lhe', u'ela', u'a',
			u'elas', u'as', u'lhes', u'elas', u'meu', u'teu', u'seu', u'nosso', u'vosso', u'minha', u'tua',
			u'sua', u'nossa', u'vossa', u'meus', u'teus', u'seus', u'nossos', u'vossos', u'seus', u'minhas',
			u'tuas', u'suas', u'nossas', u'vossas', u'tudo', u'toda', u'todo', u'todos', u'todas', u'algo', u'alguém',
			u'algum', u'alguns', u'algumas', u'um', u'uma', u'umas', u'uns', u'nada', u'ninguém', u'nenhum', u'nenhuma',
			u'nenhuns', u'nenhumas', u'mesmo', u'mesma', u'mesmos', u'mesmas', u'outrem', u'outro', u'outra',
			u'outros', u'outras', u'vários', u'várias', u'certo', u'certa', u'certos', u'certas', u'qualquer',
			u'quaisquer', u'cada', u'qual', u'quais', u'cujo', u'cuja', u'cujos', u'cujas', u'que', u'quanto',
			u'quanta', u'quantos', u'quantas', u'onde', u'dele', u'dela', u'deles', u'delas',
]

ARTIGOS = [u'o', u'a', u'os', u'as', u'do', u'da', u'dos', u'das', u'de', u'no', u'na', u'nos', u'nas', u'em',
		   u'ao', u'à', u'aos', u'às', u'a', u'pelo', u'pela', u'pelos', u'pelas', u'co', u'coa', u'cos', u'coas',
		   u'com', u'dum', u'duma', u'duns', u'dumas', u'num', u'numa', u'nuns', u'numas',
]

PREPOSICOES = [u'à', u'a', u'ante', u'até', u'após', u'com', u'contra', u'de', u'desde', u'em', u'entre', u'para',
			   u'per', u'perante', u'por', u'sem', u'sob', u'sobre', u'trás', u'afora', u'menos', u'salvo', u'conforme',
			   u'exceto', u'como', u'que', u'durante', u'neste', u'nesta', u'nestes', u'nestas', u'desse', u'dessa',
			   u'desses', u'dessas', u'deste', u'desta', u'deste', u'destas', u'diante', u'junto', u'através', u'acerca',
			   u'além', u'àquele', u'aquele', u'àquela', u'aquela', u'aquelas', u'àqueles', u'àquelas', u'aquilo', u'naquele',
			   u'àquilo', u'disso', u'daqui', u'ali', u'aqui', u'lá', u'isso', u'isto', u'esse', u'esses', u'essa', u'essas',
]

CONJUNCOES = [u'e', u'nem', u'mas', u'também', u'como', u'além', u'quanto', u'bem', u'porém', u'todavia', u'entretanto',
			  u'entanto', u'senão', u'não', u'obstante', u'contudo', u'ou', u'ora', u'já', u'quer', u'porque', u'porquanto',
			  u'pois', u'logo', u'portanto', u'então', u'isso', u'conseguinte', u'isto', u'assim', u'que', u'se',
			  u'porquanto', u'como', u'vez', u'visto', u'entre', u'outro', u'outros', u'tal', u'qual', u'embora',
			  u'conquanto', u'ainda', u'mesmo', u'posto', u'apesar', u'despeito', u'caso', u'quando', u'contanto',
			  u'salvo', u'sem', u'desde', u'dado', u'menos', u'mais', u'conforme', u'segundo', u'forma', u'maneira',
			  u'modo', u'medida', u'passo', u'enquanto', u'antes', u'depois', u'durante', u'até', u'sempre', u'nunca',
			  u'cada', u'apenas', u'mal',
]

ADVERBIOS = [u'assim', u'bem', u'mal', u'depressa', u'devagar', u'melhor', u'pior', u'abaixo', u'acima', u'dentro',
			 u'fora', u'adentro', u'afora', u'aí', u'além', u'ali', u'aqui', u'atrás', u'cá', u'embaixo', u'lá', u'longe',
			 u'perto', u'afinal', u'agora', u'amanhã' 'antes', u'ontem', u'breve', u'cedo', u'constantemente', u'depois',
			 u'enfim', u'hoje', u'imediatamente', u'já', u'jamais', u'nunca', u'sempre', u'outrora', u'tarde', u'cedo',
			 u'não', u'tampouco', u'nunca', u'negativo', u'sim', u'certamente', u'decerto', u'certo', u'errado',
			 u'acaso', u'porventura', u'possivel', u'provavel', u'talvez', u'será', u'muito', u'pouco', u'bastante',
			 u'mais', u'menos', u'demais', u'quanto', u'quão', u'quase', u'tanto', u'tanta', u'pouca', u'partir', u'muitos',
			 u'muitas', u'muita',
]

NUMERAIS = [u'um', u'dois', u'três', u'tres', u'quatro', u'cinco', u'seis', u'sete', u'oito', u'nove', u'dez',
			u'onze', u'doze', u'treze', u'quatorze', u'quinze', u'dezesseis', u'dezessete', u'dezoiro',
			u'dezenove', u'vinte', u'trinta', u'quarenta', u'cinquenta', u'cinqüenta', u'sessenta', u'setenta',
			u'oitenta', u'noventa', u'cem', u'duzentos', u'trezentos', u'quatrocentos', u'quinhentos', u'seissentos',
			u'setecentos', u'oitocentos', u'novecentos', u'mil', u'milhão', u'bilhão', u'trilhão',
			u'uma', u'duas', u'duzentas', u'trezentas', u'quatrocentas', u'quinhentas', u'seissentas',
			u'setecentas', u'oitocentas', u'novecentas', u'milhões', u'bilhões', u'trilhões',
			u'primeiro', u'segundo', u'terceiro', u'quarto', u'quinto', u'sexto', u'sétimo', u'oitavo',
			u'nono', u'décimo', u'vigésimo', u'trigésimo', u'quadragésimo', u'quincoagésimo', u'sexagésimo',
			u'septuagésimo', u'octagésimo', u'nonagésimo', u'centésimo', u'milésimo', u'milionésimo', u'bilionésimo',
			u'primeiros', u'segundos', u'terceiros', u'quartos', u'quintos', u'sextos', u'sétimos', u'oitavos',
			u'nonos', u'décimos', u'vigésimos', u'trigésimos', u'quadragésimos', u'quincoagésimos', u'sexagésimos',
			u'septuagésimos', u'octagésimos', u'nonagésimos', u'centésimos', u'milésimos', u'milionésimos', u'bilionésimos',
			u'primeira', u'segunda', u'terceira', u'quarta', u'quinta', u'sexta', u'sétima', u'oitava',
			u'nona', u'décima', u'vigésima', u'trigésima', u'quadragésima', u'quincoagésima', u'sexagésima',
			u'septuagésima', u'octagésima', u'nonagésima', u'centésima', u'milésima', u'milionésima', u'bilionésima',
			u'primeiras', u'segundas', u'terceiras', u'quartas', u'quintas', u'sextas', u'sétimas', u'oitavas',
			u'nonas', u'décimas', u'vigésimas', u'trigésimas', u'quadragésimas', u'quincoagésimas', u'sexagésimas',
			u'septuagésimas', u'octagésimas', u'nonagésimas', u'centésimas', u'milésimas', u'milionésimas', u'bilionésimas',
]

SIMBOLOS = [u'=', u'-', u'+', u'.', u',', u':', u'<', u'>', u'&', u'%', u'$', u'#', u'@', u'(', u')', u'{', u'}', u'*',
			u'?', u'!', u'"', "'", u'/', u'\\', u'|',
]

OUTRAS = [u'blender', u'Blender', u'site', u'brasil', u'Brasil', u'br', u'BR', u'data', u'hora',
		  u'oficial', u'loja', u'galeria', u'trago', u'traga', u'faço', u'faça', u'trazer', u'fazer',
		  u'trazemos', u'fazemos', u'trouxemos', u'fizemos', u'trouxeram', u'fizeram', u'conta', u'contas',
		  u'ter', u'tenho', u'temos', u'teremos', u'tivémos', u'ser', u'somos', u'fomos', u'seremos', u'desconto',
		  u'significa', u'significar', u'significamos', u'vence', u'vencer', u'vencemos', u'ter', u'temos',
		  u'tivémos', u'teremos', u'tendo', u'sendo', u'trazendo', u'tenha', u'serem', u'serão', u'aresta',
		  u'arestas', u'vértice', u'vértices', u'vertice', u'vertices', u'edge', u'edges', u'face', u'faces',
		  u'energia', u'energias', u'simples', u'fácil', u'difícil', u'fáceis', u'complexo', u'complexos',
		  u'problema', u'solução', u'ponto', u'chegar', u'chegando', u'poder', u'poderia', u'podemos', u'pode',
		  u'podem', u'poderemos', u'poderíamos', u'tende', u'tender', u'tenderá', u'sejam', u'sentido', u'objetivo',
		  u'consiste', u'baseado', u'baseamos', u'baseei', u'obter', u'obtido', u'obtida', u'valor', u'valores',
		  u'total', u'totais', u'local', u'lugar', u'início', u'fim', u'começo', u'término', u'final', u'inicial',
		  u'pessoa', u'pessoas', u'for', u'foram', u'estar', u'estava', u'estiver', u'estão', u'está', u'grupo',
		  u'maior', u'menor', u'maiores', u'menores', u'importante', u'interessante', u'legal', u'parte', u'partes',
		  u'tempo', u'haver', u'estarei', u'haviam', u'haverá', u'haverão', u'teremos', u'falar', u'falou', u'falando',
		  u'falei', u'disse', u'dizer', u'dizendo', u'dizia', u'pergunta', u'resposta', u'perguntar', u'responder',
		  u'perguntou', u'perguntaram', u'perguntam', u'havia', u'respondeu', u'responderam', u'respondem', u'responde',
		  u'ficar', u'fica', u'ficam', u'ficou', u'ficaram', u'ficaremos', u'ficarei', u'andar', u'anda', u'andamos',
		  u'andei', u'vimos', u'veremos', u'continua', u'parou', u'parado', u'continando', u'continuei', u'continuamos',
		  u'tinha', u'tinhamos', u'teremos', u'tínhamos', u'coisa', u'coisas', u'grande', u'grandes', u'pequeno',
		  u'pequenos', u'pequena', u'pequenas', u'velho', u'velhos', u'novo', u'novos', u'velha', u'velhas', u'nova', u'novas',
		  u'andar', u'andei', u'andam', u'andamos', u'andou', u'andando', u'andaremos', u'continuar', u'continuam', u'fatos',
		  u'parecer', u'parece', u'parecem', u'parecia', u'pareceu', u'horas', u'hora', u'tempo', u'homem', u'mulher',
		  u'homens', u'mulheres', u'velocidade', u'fundo', u'volta', u'voltas', u'senhor', u'senhora', u'senhoria',
		  u'menino', u'menina', u'metros', u'metro', u'dias', u'meses', u'semanas', u'semana', u'podia', u'estar',
		  u'estou', u'estamos', u'estive', u'estivemos', u'gente', u'causa', u'motivo', u'razão', u'contar', u'dizer',
		  u'dizem', u'digam', u'falem', u'verdade', u'mentira', u'verdades', u'mentiras', u'verdadeiro', u'falso',
		  u'verdadeiros', u'falsos', u'claro', u'escuro', u'claros', u'escuros', u'sentir', u'senti', u'sinto',
		  u'garota', u'fiquei', u'queria', u'querer', u'quero', u'queremos', u'querendo', u'jeito', u'forma', u'maneira',
		  u'começo', u'começar', u'comecei', u'terminei', u'fosse', u'seria', u'serão', u'saber', u'souber', u'ficava',
		  u'teria', u'fazia', u'passar', u'passei', u'passamos', u'passarei', u'passaremos', u'pedir', u'pedirei', u'pediram',
		  u'pedido', u'pedidos', u'tirar', u'tirei', u'levar', u'levei', u'levamos', u'conseguir', u'consegui', u'conseguimos',
		  u'colocar', u'colocarei', u'coloquei', u'colocamos', u'monte', u'saber', u'sabia', u'saberei', u'saberá',
		  u'vezes', u'frente', u'estavam', u'tivesse', u'tivessem', u'encontrar', u'deixar', u'voltar', u'voltei',
		  u'voltamos', u'achar', u'encontrar', u'achei', u'acohou', u'achamos', u'encontrei', u'encontramos', u'cheguei',
		  u'tinham', u'pegar', u'peguei', u'pegamos', u'pegou', u'fazendo', u'virar', u'virou', u'resolvi', u'deixar',
		  u'deixei', u'deixamos', u'cheio', u'cheia', u'cheios', u'cheias', u'vazio', u'vazia', u'vazios', u'vazias',
		  u'conseguiu', u'certeza', u'dúvida', u'perguntas', u'tentar', u'tentei', u'tentou', u'tentamos', u'dever',
		  u'deverá', u'deveria', u'devia', u'posso', u'gosto', u'gostei', u'gostaria',
]

def deve_ignorar(palavra, dict):
	palavra = palavra.replace(',', '')
	palavra = palavra.replace('.', '')
	palavra = palavra.replace(':', '')
	palavra = palavra.replace("'", '')
	palavra = palavra.replace('"', '')
	if palavra in dict.keys():
		return True
	lista = PRONOMES + ARTIGOS + PREPOSICOES + CONJUNCOES + ADVERBIOS + NUMERAIS + SIMBOLOS + OUTRAS
	if len(palavra) < 5:
		return True
	if palavra in lista:
		return True
	if palavra.lower() in lista:
		return True;
	if palavra+u's' in lista:
		return True
	if palavra.endswith(u'mente'):
		return True
	if palavra.endswith(u'°') or palavra.endswith(u'º') or palavra.endswith(u'ª'):
		return True
	try:
		unicode(palavra)
	except:
		return True
	try:
		int(palavra)
		return True
	except:
		pass
	try:
		float(palavra)
		return True
	except:
		pass
	return False
	
def keywords(texto, limite=8):
	if texto:
		texto = texto.replace('\n', '')
		texto = texto.replace('\r', '')
		texto = texto.replace(',', '')
		texto = texto.split()
		top_palavras = {}
	
		for palavra in texto:
			if not palavra in top_palavras.keys():
				if not deve_ignorar(palavra, top_palavras):
					top_palavras[palavra] = 1
			else:
				top_palavras[palavra] += 1
	
		top_palavras = sorted(top_palavras.items(), key=itemgetter(1))
		top_palavras.reverse()
		top_palavras = [p[0] for p in top_palavras[:limite]]
		return KEYWORDS_PADRAO + top_palavras
	return KEYWORDS_PADRAO

def description(texto, limite=130):
	if texto:
		return texto[:limite]
	return DESCRIPTION_PADRAO