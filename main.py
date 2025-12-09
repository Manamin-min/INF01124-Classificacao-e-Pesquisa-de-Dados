import csv
import pandas as pd
import math
import time

#2.1 - Estrutura 1: Armazenando dados sobre filmes (Tabela hash)
class TabelaHash:
    def __init__(self):
        self.buckets = []
        for i in range(10):                 #itera de 0 a 9
            self.buckets.append([])

    def criarHash(self, movieId):           #achar o indice da tabela
        return movieId % 10

    def add(self, movieId, movie):          #adiciona o FILME (inteiro) na hash
        hash = self.criarHash(movieId)
        self.buckets[hash].append(movie)
            
    def get(self, movieId):                 #passo o id e me retorna o filme com esse id
        hash = self.criarHash(movieId)
        bucket = self.buckets[hash]
        for filme in bucket: 
            if filme.movieId == movieId:
                return filme
            
    def attRating(self, movieId, rating):   #calcula a media dos valores das avaliações
        movie = self.get(movieId)
        movie.somaRatings += rating 
        movie.totalRatings += 1
        movie.mediaRatings = movie.somaRatings / movie.totalRatings
        return movie.mediaRatings
                   
class Filme:                                    
    def __init__(self, movieId, movieName, movieGenre, movieYear):
        self.movieId = movieId
        self.movieName = movieName
        self.movieGenre = movieGenre
        self.movieYear = movieYear
        self.totalRatings = 0
        self.mediaRatings = 0
        self.somaRatings = 0

#para nao aparecer o numero do endereco
    def __str__(self):
        return f"Filme: {self.movieName}, ID = {self.movieId}, Genero: {self.movieGenre}, Ano: {self.movieYear}, Média = {self.mediaRatings})"

    def __repr__(self):
        return f"Filme: {self.movieName}, ID = {self.movieId}, Genero: {self.movieGenre}, Ano: {self.movieYear}, Média = {self.mediaRatings})"

tabelahash = TabelaHash()

#le os dados e popula - filmes
df = pd.read_csv("movies.csv")
for index, row in df.iterrows():            
    tabelahash.add(row ["movieId"], Filme(row ["movieId"], row ["title"], row ["genres"], row ["year"]))

#le os dados e popula - avaliações
df = pd.read_csv("miniratings.csv")
for index, row in df.iterrows():
    tabelahash.attRating(row ["movieId"], row ["rating"])

# print(tabelahash.buckets)
# print(tabelahash.get(12))

#2.2 - Estrutura 2: Estrutura para buscar por strings de nomes (TRIE, Radix Tree, TST)
class NodoTrieFilmes:
    def __init__(self):
        self.filhos = [None] * 256
        self.idf = None
        self.fim = False
class ArvoreTrieFilmes:
    def __init__(self):
        self.raiz = NodoTrieFilmes()

def trie_busca_prefixo_aux(raiz, ids):
    if raiz.fim:
        ids.append(raiz.idf)
    for i in range(256):
        if raiz.filhos[i] is not None:
            trie_busca_prefixo_aux(raiz.filhos[i], ids)
    return

def trie_busca_prefixo(raiz, prefix):
    atual = raiz
    for letra in prefix:
        i = ord(letra) % 256
        if atual.filhos[i] is None:
            return None
        atual = atual.filhos[i]
    ids = []
    trie_busca_prefixo_aux(atual, ids) 
    if ids:
        return ids
    return None

def busca_por_prefixo(prefix, trie, th):
    filmes_encontrados = trie_busca_prefixo(trie, prefix)
    res = []
    if filmes_encontrados is not None:
        for filme in filmes_encontrados:
            if th.get(filme) is not None:
                res.append(th.get(filme)) # coloca na matriz as informações de cada filme
        return res
    return None

def counting_sort(arr, val):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = int((arr[i] * (10**6)) // val) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = int((arr[i] * (10**6)) // val) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    return output

def lsd_radix_sort(arr):
    max_val = int(max(arr)*(10**6))
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort(arr, exp)
        exp *= 10
    return arr

def selection_sort_1(filmes):
    n = len(filmes)
    for i in range(n):
        max = i
        for j in range(i+1, n):
            if filmes[j][6] > filmes[max][6]:
                max = j
            elif filmes[j][6]==filmes[max][6] and filmes[j][5] > filmes[max][5]:
                max = j
        filmes[i], filmes[max] = filmes[max], filmes[i]
    return filmes

def selection_sort(filmes):
    n = len(filmes)
    for i in range(n):
        max = i
        for j in range(i+1, n):
            if filmes[j][5] > filmes[max][5]:
                max = j
            elif filmes[j][5]==filmes[max][5] and filmes[j][4]>filmes[max][4]:
                max = j
        filmes[i], filmes[max] = filmes[max], filmes[i]
    return filmes

def le_filmes_csv(nome):
    df = pd.read_csv(nome, encoding='utf-8')
    df['genres'] = df['genres'].str.split('|')
    df = df[['title', 'movieId', 'genres', 'year']]
    matriz = df.values.tolist()
    for linha in matriz:
        linha.extend([0, 0])
    return matriz

def insere_nodo_trie(raiz, palavra, chave):
    atual = raiz
    for letra in palavra:
        i = ord(letra) % 256
        if atual.filhos[i] is None:
            atual.filhos[i] = NodoTrieFilmes()
        atual = atual.filhos[i]
    atual.idf = chave
    atual.fim = True

trie_filmes = ArvoreTrieFilmes()

dados_filmes_movies = le_filmes_csv("movies.csv")
if dados_filmes_movies:
    for titulo, id_f, generos, ano, quant_av, media_av in dados_filmes_movies:
        insere_nodo_trie(trie_filmes.raiz, titulo, id_f)

print(trie_filmes)
print(busca_por_prefixo("Dra", trie_filmes.raiz, tabelahash))

#2.3 - Estrutura 3: Estrutura para guardar revisões de usuários
class Reviews:
    def __init__(self, movieId, rating, date):
        self.movieId = movieId
        self.rating = rating
        self.date = date

    def __str__(self):
        return f"ID-Filme: {self.movieId}, Avaliação = {self.rating}, Data: {self.date})"

    def __repr__(self):
        return f"ID-Filme: {self.movieId}, Avaliação = {self.rating}, Data: {self.date})"      

class ReviewUser:
    def __init__ (self, userId):
        self.userId = userId
        self.reviews = []

    def __str__(self):
        return f"User: {self.userId}, Review = {self.reviews})"

    def __repr__(self):
        return f"User: {self.userId}, Review = {self.reviews})"
    
class TabelaHashReviews:
    def __init__(self):
        self.buckets = []
        for i in range(10):                 #itera de 0 a 9
            self.buckets.append([])

    def criarHash(self, userId):           #achar o indice da tabela hash - user
        return userId % 10

    def add(self, userId, review):          #checa se existe
        hash = self.criarHash(userId)
        bucket = self.buckets[hash]
        userReview = self.get(userId)
        if userReview == None:
            userReview = ReviewUser(userId)
            bucket.append(userReview)
        userReview.reviews.append(review)
            
    def get(self, userId):                 #passo o id e me retorna o filme com esse id
        hash = self.criarHash(userId)
        bucket = self.buckets[hash]
        for review in bucket: 
            if review.userId == userId:
                return review
        return None 

tabelahashreviews = TabelaHashReviews()

df = pd.read_csv("miniratings.csv")
for index, row in df.iterrows():
    tabelahashreviews.add(row ["userId"], Reviews(row ["movieId"], row ["rating"], row ["date"]))
                   
# print(tabelahashreviews.buckets)
# print(tabelahashreviews.get(1))

#2.4 - Estrutura 4: Estrutura para guardar tags
class Tags:
    def __init__(self, tag):
        self.tag = tag
        self.movieIds = []

    def __str__(self):
        return f"Tag: {self.tag}, MovieIds: {self.movieIds})"

    def __repr__(self):
        return f"Tag: {self.tag}, MovieIds: {self.movieIds})"

class TabelaHashTags:
    def __init__(self):
        self.buckets = []
        for i in range(10):                 #itera de 0 a 9
            self.buckets.append([])

    def criarHash(self, tag):
        return sum(ord(c) for c in str(tag))%10
    
    def add(self, movieId, tag):          #cria a hash pela tag, adiciona o filme e a tag
        hash = self.criarHash(tag)
        bucket = self.buckets[hash]
        filmesPorTag = self.get(tag)           #pega a coleção de filmes por tag
        if filmesPorTag == None:
            filmesPorTag = Tags(tag)
            bucket.append(filmesPorTag)
        filmesPorTag.movieIds.append(movieId)
            
    def get(self, tag):                 #passo o tag e me retorna o filme com esse id
        hash = self.criarHash(tag)
        bucket = self.buckets[hash]
        for filmePorTag in bucket: 
            if filmePorTag.tag == tag:
                return filmePorTag
        return None
            
tabelahashtags = TabelaHashTags()

df = pd.read_csv("tags.csv")
for index, row in df.iterrows():
    tabelahashtags.add(row ["movieId"], row ["tag"])

# print(tabelahashtags.buckets)
# print(tabelahashtags.get(12))