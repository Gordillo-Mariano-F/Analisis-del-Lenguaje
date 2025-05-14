# Importamos las bibliotecas necesarias
import nltk
import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer

# Lectura y procesamiento del archivo CorpusLenguajes.txt
with open("CorpusLenguajes.txt", encoding="utf-8") as archivo:
    contenido = archivo.read()

# Extracción de oraciones específicas dentro de paréntesis y comillas
oraciones_filtradas = re.findall(r'\("([^"]*?)"\)', contenido)
texto_consolidado = " ".join(oraciones_filtradas)

# Función de tokenización
def tokenizar_texto(texto):
    return word_tokenize(texto)

tokens = tokenizar_texto(texto_consolidado)
print("Tokens generados:", tokens)

# Función para eliminar palabras vacías (stopwords)
def remover_stopwords(texto):
    palabras_vacias = stopwords.words("english")
    return [
        palabra.lower() for palabra in texto
        if palabra.lower() not in palabras_vacias
        and palabra not in string.punctuation
        and not any(simbolo in palabra for simbolo in ["|", "--", "''", "``", "()", "_", "-"])
    ]

texto_filtrado = remover_stopwords(tokens)
print("\nTexto sin stopwords:", texto_filtrado)

# Función para obtener el tipo de palabra según WordNet
def determinar_pos_palabra(palabra):
    etiqueta = nltk.pos_tag([palabra])[0][1][0].upper()
    tipos = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tipos.get(etiqueta, wordnet.NOUN)

# Función de lematización
def aplicar_lematizacion(texto):
    lematizador = WordNetLemmatizer()
    return [lematizador.lemmatize(palabra, determinar_pos_palabra(palabra)) for palabra in texto]

texto_lema = aplicar_lematizacion(texto_filtrado)
print("\nTexto lematizado:", texto_lema)

# Aplicación de TF-IDF
vectorizador = TfidfVectorizer()
matriz_tfidf = vectorizador.fit_transform(oraciones_filtradas)
print("\nMatriz TF-IDF:\n", matriz_tfidf.toarray())
print("\nVocabulario TF-IDF:\n", vectorizador.get_feature_names_out())

# Análisis de palabras más usadas y menos usadas
frecuencia_palabras = FreqDist(aplicar_lematizacion(remover_stopwords(tokens)))
palabras_frecuentes = frecuencia_palabras.most_common(6)
print("\nSeis palabras más usadas:", palabras_frecuentes)
palabra_menos_frecuente = min(frecuencia_palabras, key=frecuencia_palabras.get)
print(f"\nLa palabra menos utilizada es: '{palabra_menos_frecuente}'")

# Análisis de palabras más repetidas en cada oración
for indice, oracion in enumerate(oraciones_filtradas):
    tokens_oracion = aplicar_lematizacion(remover_stopwords(word_tokenize(oracion)))
    frecuencia_oracion = FreqDist(tokens_oracion)
    palabra_mas_comun = frecuencia_oracion.most_common(1)

    if palabra_mas_comun:
        print(f"\nEn la oración {indice + 1}, la palabra más repetida es: '{palabra_mas_comun[0][0]}' con frecuencia de {palabra_mas_comun[0][1]}")

# Gráficos de frecuencia
frecuencia_palabras = FreqDist(tokens)
frecuencia_palabras.plot(20, show=True)

frecuencia_palabras_filtradas = FreqDist(aplicar_lematizacion(remover_stopwords(texto_filtrado)))
frecuencia_palabras_filtradas.plot(20, show=True)