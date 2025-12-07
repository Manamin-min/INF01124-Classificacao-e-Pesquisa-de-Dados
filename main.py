import csv
import pandas as pd

df = pd.read_csv("movies.csv")#
# print(df)

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
                   
class Filme:                                    
    def __init__(self, movieId, movieName, movieGenre, movieYear):
        self.movieId = movieId
        self.movieName = movieName
        self.movieGenre = movieGenre
        self.movieYear = movieYear


#para nao aparecer o numero do endereco
    def __str__(self):
        return f"Filme: {self.movieName}, ID = {self.movieId}, Genero: {self.movieGenre}, Ano: {self.movieYear})"

    def __repr__(self):
        return f"Filme: {self.movieName}, ID = {self.movieId}, Genero: {self.movieGenre}, Ano: {self.movieYear})"
    

tabelahash = TabelaHash()


for index, row in df.iterrows():
    tabelahash.add(row ["movieId"], Filme(row ["movieId"], row ["title"], row ["genres"], row ["year"]))


print(tabelahash.buckets)
print(tabelahash.get(12))

