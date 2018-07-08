from flask import Flask, render_template, request
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd
import json
import webbrowser
import numpy as np
import math
import copy

# algorithm :
# 1. take input from user
# 2. tf-idf the input, further information on ppt
# 3. compare result with ones from database / json

app = Flask(__name__, static_url_path = "/images", static_folder = "images")

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def process():
	if request.method == 'GET':
		return render_template('result.html')

	elif request.method =='POST':
		keyword = request.form['keyword']
		kataDepan = pd.read_csv("data/konjungsi.csv")
		kataDepan = kataDepan.values.tolist()
		datasets = pd.read_csv("data/datasets.csv")
		dokumen = datasets.values.tolist()
		index = pd.read_csv("data/index.csv")
		index = index.values.tolist()
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		result = [[] for i in range(len(dokumen))]
		data = []
		corpus = len(dokumen)

		kata = stemmer.stem(keyword)
		temp = set(kata.split())
		temp = list(temp)

		# eliminating prepositions if there are any
		tfidf = [[x] for x in temp]
		index = [x for x in index if x[0] in temp]
		kata = [[x] for x in temp if x not in kataDepan]
		scores = [[l+1, 0.0] for l in range(30)]
		magnitude = [[l+1, 0.0] for l in range(30)]
		finalScores = [[l+1, 0.0] for l in range(30)]

		temp = keyword.split()

		for x in kata:
			x.append(temp.count(x[0]))

		index = sorted(index, key=lambda x: x[0])
		kata = sorted(kata, key=lambda x: x[0])
		tfidf = sorted(tfidf, key=lambda x: x[0])

		# print(kata)


		for i in range(len(tfidf)):
			try:
				tfidf[i].append(kata[i][1] * (1 + math.log(corpus/(((corpus-(index[i].count(0))))+1))))
				print((1 + math.log(corpus/(((corpus-(index[i].count(0))))+1))))
			except IndexError:
				continue

		print(tfidf)

		# tfidf dokumen
		for i in range(len(scores)):
			try:
				temp = 0
				for n in range(len(kata)):
					if index[n][i+1] != 0 :
						scores[i][1] += tfidf[n][1] * (index[n][i+1] * 1 + math.log(corpus+1/(((corpus-(index[n].count(0))))+1)))
						magnitude[i][1] += math.pow(index[n][i+1] * 1 + math.log(corpus+1/(((corpus-(index[n].count(0))))+1)),2)
			except IndexError:
				continue

		for i in range(len(finalScores)):
			if magnitude[i][1] != 0:
				finalScores[i][1] = (scores[i][1])/(math.sqrt(magnitude[i][1]))

		print(scores)
		print(magnitude)
		print(finalScores)

		finalScores = sorted(finalScores, key=lambda x: x[1], reverse=True)

		print(finalScores)

		for i in range(len(finalScores)):
			if finalScores[i][1] > 0:
				data.append(dokumen[finalScores[i][0]-1])

		return render_template('result.html', keyword=keyword, data=data)

# run app
if __name__ == "__main__":
    app.run(debug=True)