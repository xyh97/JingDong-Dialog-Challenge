# -*- coding: utf-8 -*-
import jieba
from tfidf.util import read_lines

_STOP_WORDS_FP = 'stop_words.txt'


class Tokenizer:
    def __init__(self):
        self.stop_words = [i for i in read_lines(_STOP_WORDS_FP) if i]

    def cut_for_search(self, sentence, filter_stop_word=True):
        tokens = jieba.cut_for_search(sentence)
        return [t for t in tokens if (not filter_stop_word) or (t not in self.stop_words)]


if __name__ == '__main__':
    tokenizer = Tokenizer()
    text = '清华大学离世界一流大学有一条街的距离'
    print('origin:', text)
    print('cutted:', tokenizer.cut_for_search(sentence=text))
