import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk

# Descargar stopwords de español (solo la primera vez)
nltk.download('stopwords')
palabras_vacias = set(stopwords.words('spanish'))

# === Leer archivo de texto ===
def cargar_corpus(path):
    with open(path, encoding="latin-1") as f:
        return f.read()

# === Preprocesar: minúsculas, quitar signos y números ===
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\d+", "", texto)
    return texto

# === Tu función personalizada para filtrar tokens ===
def filtrar_tokens(texto):
    return [
        palabra for palabra in texto
        if palabra not in palabras_vacias
        and palabra not in string.punctuation
        and not any(simbolo in palabra for simbolo in ["|", "--", "''", "``", "()", "_", "-"])
    ]

# === Generar DataFrame con ngramas frecuentes ===
def obtener_ngrams(tokens, n=2, min_count=2):
    texto_final = " ".join(tokens)
    vectorizer = CountVectorizer(ngram_range=(n, n))
    X = vectorizer.fit_transform([texto_final])
    frecs = X.toarray().sum(axis=0)
    palabras = vectorizer.get_feature_names_out()
    df = pd.DataFrame({"ngrama": palabras, "frecuencia": frecs})
    return df[df["frecuencia"] >= min_count].sort_values("frecuencia", ascending=False)


# === Graficar top ngramas ===
def graficar(df, titulo):
    df.head(15).plot(kind="bar", x="ngrama", y="frecuencia", figsize=(10,4), color="mediumseagreen")
    plt.title(titulo)
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# === Flujo principal ===
if __name__ == "__main__":
    texto = cargar_corpus("CorpusEducacion.txt")
    limpio = limpiar_texto(texto)
    tokens = filtrar_tokens(limpio.split())

    bigramas = obtener_ngrams(tokens, n=2, min_count=2)
    trigramas = obtener_ngrams(tokens, n=3, min_count=2)

    graficar(bigramas, "Top 2-gramas (min_df=2)")
    graficar(trigramas, "Top 3-gramas (min_df=2)")