import csv
import pandas as pd


#2.1 - Estrutura 1: Armazenando dados sobre filmes (Tabela hash)
class TabelaHash:
    def __init__(self):
        self.buckets = []
        for i in range(10):                 #itera de 0 a 9
            self.buckets.append([])

    def criarHash(self, movieId):           #achar o indice da tabela
        return movieId % 10

    def add(self, movieId, movie):          #adiciona o FILME (interiro) na hash
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


                   
print(tabelahashreviews.buckets)
print(tabelahashreviews.get(1))
#2.4 - Estrutura 4: Estrutura para guardar tags

