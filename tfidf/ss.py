# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
from tfidf.sentence import Sentence
from collections import defaultdict
from queue import PriorityQueue


class SentenceSimilarity:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def set_tokenized_questions(self, questions):
        self.questions = questions

    # 构建其他复杂模型前需要的简单模型
    def simple_model(self, min_frequency=1):
        self.texts = self.questions

        # 删除低频词
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1

        self.texts = [[token for token in text if frequency[token] > min_frequency] for text in
                      self.texts]

        self.dictionary = corpora.Dictionary(self.texts)
        self.corpus_simple = [self.dictionary.doc2bow(text) for text in self.texts]

    # tfidf模型
    def TfidfModel(self):
        self.simple_model()

        # 转换模型
        self.model = models.TfidfModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]

        # 创建相似度矩阵
        self.index = similarities.MatrixSimilarity(self.corpus)

    def sentence2vec(self, sentence):
        sentence = Sentence(sentence, self.tokenizer)
        vec_bow = self.dictionary.doc2bow(sentence.sentence)
        return self.model[vec_bow]

    # 求最相似的句子
    def similarity(self, sentence):
        sentence_vec = self.sentence2vec(sentence)
        sims = self.index[sentence_vec]

        # 维护一个优先队列存储 top15
        que = PriorityQueue()
        q_size = 0
        similarity_at_15 = -1
        for index, similarity in enumerate(sims):
            if similarity > similarity_at_15 or q_size < 15:
                que.put((similarity, index))
                v, i = que.get()
                similarity_at_15 = v
                if q_size < 15:
                    que.put((v, i))
                    q_size += 1

        top_15 = []
        while not que.empty():
            top_15.append(que.get())
        top_15 = top_15[::-1]

        return top_15
