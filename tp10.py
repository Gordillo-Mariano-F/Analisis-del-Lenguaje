from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# Documentos sobre animales
documents = [
    "El veloz zorro marrón salta sobre el perro perezoso.",
    "Un perro marrón persiguió al zorro.",
    "El perro es perezoso."
]

# Convertir documentos a vectores TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Calcular la matriz de similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Mostrar matriz como tabla
print("Matriz de Similitud del Coseno:")
print(cosine_sim)

# Graficar matriz
plt.figure(figsize=(6, 5))
sns.heatmap(cosine_sim, annot=True, cmap="YlGnBu",
            xticklabels=["Doc1", "Doc2", "Doc3"],
            yticklabels=["Doc1", "Doc2", "Doc3"])
plt.title("Matriz de Similitud entre Documentos")
plt.show()