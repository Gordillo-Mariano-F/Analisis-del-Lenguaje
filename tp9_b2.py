import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords

# Descargar stopwords si no están
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# Documentos sobre civilizaciones antiguas
documents = {
    "doc1": "Los egipcios construyeron las pirámides y desarrollaron una escritura jeroglífica.",
    "doc2": "La civilización romana fue una de las más influyentes en la historia occidental.",
    "doc3": "Los mayas eran expertos astrónomos y tenían un avanzado sistema de escritura.",
    "doc4": "La antigua Grecia sentó las bases de la democracia y la filosofía moderna.",
    "doc5": "Los sumerios inventaron la escritura cuneiforme y fundaron las primeras ciudades.",
}

# Tokenizador sin dependencia de punkt
tokenizer = TreebankWordTokenizer()
stop_words = set(stopwords.words("spanish"))

# Preprocesamiento
def preprocess(text):
    tokens = tokenizer.tokenize(text.lower())
    return set([word for word in tokens if word.isalnum() and word not in stop_words])

# Crear índice invertido
index = {}
for doc_id, text in documents.items():
    for word in preprocess(text):
        index.setdefault(word, set()).add(doc_id)

# Búsqueda booleana
def boolean_search(query):
    terms = query.lower().split()
    result_set = set(documents.keys())
    i = 0
    while i < len(terms):
        term = terms[i]
        if term in ["and", "or", "not"]:
            i += 1
            if i >= len(terms): break
            next_words = preprocess(terms[i])
            docs = set()
            for word in next_words:
                docs |= index.get(word, set())
            if term == "and":
                result_set &= docs
            elif term == "or":
                result_set |= docs
            elif term == "not":
                result_set -= docs
        else:
            docs = set()
            for word in preprocess(term):
                docs |= index.get(word, set())
            result_set &= docs
        i += 1
    return result_set

# Búsqueda interactiva
print("📘 Buscador Booleano – Civilizaciones Antiguas")
print("Usá operadores AND, OR, NOT | Escribí 'salir' para terminar")

while True:
    consulta = input("\n🔎 Ingrese una consulta booleana: ").strip().lower()
    if consulta == "salir":
        print("👋 ¡Hasta la próxima!")
        break
    resultados = boolean_search(consulta)
    if resultados:
        print("✅ Documentos encontrados:", resultados)
    else:
        print("⚠️ No se encontraron coincidencias.")
