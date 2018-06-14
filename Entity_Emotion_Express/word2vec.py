#encoding=utf-8
from gensim.models import word2vec

path = './CCF_data/data.ori.pos.w2v'
sentences=word2vec.Text8Corpus(path)
model=word2vec.Word2Vec(sentences,min_count=5,size=100)
# model.save('./CCF_data/word2vec_model')
model.wv.save_word2vec_format("word2vec.model.txt", binary=False)
