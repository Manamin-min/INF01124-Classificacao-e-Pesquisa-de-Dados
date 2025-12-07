import csv
import pandas as pd

df = pd.read_csv("movies.csv")#
# print(df)

# for index, row in df.iterrows():
#     print(index)
#     print(row)
#     print(row["userId"], row["movieId"])  # acessar por coluna


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
            
    def get(self, movieId):                 #compara o filme do hash com o filme da classe, basicamente pega o filme da tabela e retorna as informacoes especificas
        hash = self.criarHash(movieId)
        bucket = self.buckets[hash]
        for filme in bucket: 
            if filme.movieId == movieId:
                return filme
    
                
class Filme:                                    
    def __init__(self, movieId, movieName):
        self.movieId = movieId
        self.movieName = movieName

#para nao aparecer o numero do endereco
    def __str__(self):
        return f"filme(name={self.movieName}, id={self.movieId})"

    def __repr__(self):
        return f"filme(name={self.movieName}, id={self.movieId})"
    
tabelahash = TabelaHash()

tabelahash.add(0, Filme(0, "Rei Leao"))
tabelahash.add(1, Filme(1, "Rei Leao1"))
tabelahash.add(2, Filme(2, "Rei Leao2"))
tabelahash.add(12, Filme(12, "Rei Leao12"))

print(tabelahash.buckets)
print(tabelahash.get(12))

