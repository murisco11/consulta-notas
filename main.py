import numpy as np
import pandas as pd
import spacy as sp
import unicodedata

alunos = pd.read_csv("alunos.csv")
alunos.index.name = None

def texto_normalizado(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    return text

nlp = sp.load('pt_core_news_sm')

materias = ["historia", "geografia", "matematica", "portugues", "ciencias", "ingles"]
series = ["primeira", "segunda", "terceira", "quarta", "quinta"]

def sistema(mensagem):
    doc = nlp(mensagem)

    serie = None
    materia = None

    for token in doc:
        if token.text in materias:
            materia = token.text
        if token.text in series:
            serie = token.text

    if not materia:
        return "Não foi possível encontrar a matéria mencionada."
    
    if not serie:
        return "Não foi possível encontrar a série mencionada."

    keywords_quantidade = ["quantidade", "quantas pessoas", "quantos alunos"]
    keywords_media = ["media", "média"]
    keywords_maior = ["maior", "maior nota"]
    keywords_menor = ["menor", "menor nota"]

    if any(keyword in mensagem for keyword in keywords_quantidade):
        if serie:
            return f"A quantidade de alunos matriculados na {serie} série é: {quantidade_alunos(serie)}"
        else:
            return f"A quantidade de alunos matriculados na escola é: {quantidade_alunos()}"
    
    elif any(keyword in mensagem for keyword in keywords_media):
        if serie:
            return f"Aqui está a média da matéria {materia}: {media(materia, serie)} na {serie} série"
        else:
            return f"Aqui está a média da matéria {materia}: {media(materia)} em toda a escola"
        
    elif any(keyword in mensagem for keyword in keywords_maior):
        if serie:
            return f"Aqui está a maior nota da matéria {materia}: {maior_nota(materia, serie)} na {serie} série"
        else:
            return f"Aqui está a maior nota da matéria {materia}: {maior_nota(materia)} em toda a escola"
    
    elif any(keyword in mensagem for keyword in keywords_menor):
        if serie:
            return f"Aqui está a menor nota da matéria {materia}: {menor_nota(materia, serie)} na {serie} série"
        else:
            return f"Aqui está a menor nota da matéria {materia}: {menor_nota(materia)} em toda a escola"

    return "Não entendi a sua pergunta, pode reformular?"

def media(materia, serie=None):
    if serie is None:
        return alunos[materia].mean()
    else:
        return np.float64(alunos[alunos["série"] == serie][materia].mean())

def maior_nota(materia, serie=None):
    if serie is None:
        return alunos[materia].max()
    else:
        return notas_cfg(materia, serie, maior=True)

def menor_nota(materia, serie=None):
    if serie is None:
        return alunos[materia].min()
    else: 
        return notas_cfg(materia, serie, maior=False)

def quantidade_alunos(serie=None):
    if serie is None:
        return alunos['nome'].count()
    else:
        alunos_serie = alunos[alunos['série'] == serie]
        return alunos_serie["nome"].count()

def notas_cfg(materia, serie, maior=True):
    alunos_serie = alunos[alunos['série'] == serie]
    
    if maior:
        nota = alunos_serie[materia].max()
    else:
        nota = alunos_serie[materia].min()
    
    alunos_com_nota = alunos_serie[alunos_serie[materia] == nota]
    nomes_alunos = ", ".join(alunos_com_nota['nome'].values)
    
    return f"Nota {nota}, obtida pelos alunos: {nomes_alunos}"

mensagem = texto_normalizado(input("Faça a pergunta, por favor: "))
resultado = sistema(mensagem)
print(resultado)