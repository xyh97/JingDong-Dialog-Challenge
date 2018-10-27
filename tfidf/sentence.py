# -*- coding: utf-8 -*-
from tfidf.tokenizer import Tokenizer


class Sentence:
    def __init__(self, sentence, tokenizer: Tokenizer, sid=0):
        self.id = sid
        self.origin = sentence
        self.sentence = tokenizer.cut_for_search(sentence)
