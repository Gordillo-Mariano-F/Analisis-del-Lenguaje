import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords

# Asegurar ruta correcta a los recursos NLTK
nltk.data.path.append("C:/Users/QueresUnMate/AppData/Roaming/nltk_data")

# Descargar stopwords si hace falta
nltk.download('stopwords')

# Documentos de ejemplo
documents = {
    "doc1": "La inteligencia artificial está revolucionando la tecnología.",
    "doc2": "El aprendizaje automático es clave en la inteligencia artificial.",
    "doc3": "Procesamiento del lenguaje natural y redes neuronales.",
    "doc4": "Las redes neuronales son fundamentales en deep learning.",
    "doc5": "El futuro de la IA está en el aprendizaje profundo.",
}

# Tokenizador sin dependencia de punkt_tab
tokenizer = TreebankWordTokenizer()

# Stopwords en español
stop_words = set(stopwords.words('spanish'))

# Preprocesamiento
def preprocess(text):
    tokens = tokenizer.tokenize(text.lower())
    return set([word for word in tokens if word.isalnum() and word not in stop_words])

# Crear índice invertido
index = {}
for doc_id, text in documents.items():
    words = preprocess(text)
    for word in words:
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
            words = preprocess(term)
            docs = set()
            for word in words:
                docs |= index.get(word, set())
            result_set &= docs
        i += 1
    return result_set

# Búsqueda interactiva
print("📘 Buscador Booleano Activo. Escribí tu consulta usando AND, OR, NOT.")
print("🔚 Escribí 'salir' para terminar.")

while True:
    consulta = input("\n🔎 Ingrese una consulta booleana: ").strip().lower()
    if consulta == 'salir':
        print("👋 ¡Hasta la próxima!")
        break
    resultados = boolean_search(consulta)
    if resultados:
        print("✅ Documentos encontrados:", resultados)
    else:
        print("⚠️ No se encontraron coincidencias.")
