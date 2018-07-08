from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from collections import Counter
import pandas as pd
import numpy as np
import math
import copy

kataDepan = pd.read_csv("data/konjungsi.csv")
kataDepan = kataDepan.values.tolist()
datasets = pd.read_csv("data/datasets.csv")
dokumen = datasets.values.tolist()
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stemmedDoc, index = [], []

for baris in dokumen:
	arrayTempBaris = baris[3].split()

	# 2 - Filtering - cek bila kata memiliki kata depan yang harus dihapus
	arrayTempBaris = [x for x in arrayTempBaris if x not in kataDepan]
	tempBaris = " ".join(arrayTempBaris)

	# 3 - Stemming - menghapus awalan
	tempBaris = stemmer.stem(tempBaris)
	stemmedDoc.append(tempBaris.split())

for record in stemmedDoc:
	for kata in record:
		if kata not in index:
			index.append(kata)

df_index = pd.DataFrame({
	'kata':index
	})

for i in range(len(stemmedDoc)):
	terdeteksi = []
	for kata in index:
		terdeteksi.append(stemmedDoc[i].count(kata))
	df_index[i+1] = pd.Series(terdeteksi)

df_index['total'] = df_index.sum(axis=1)

print(df_index)

df_index.to_csv("data/index.csv", index=False)