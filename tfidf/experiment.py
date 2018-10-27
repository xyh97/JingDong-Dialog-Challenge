# -*- coding: utf-8 -*-
from tfidf.tokenizer import Tokenizer
from tfidf.ss import SentenceSimilarity
from tfidf.util import read_lines, get_path
import re
import pickle


def predict(input_fp):
    with open(get_path('processed/tokenized_questions.pkl'), 'rb') as f:
        train_tokenized_questions = pickle.load(f)

    train_answers = read_lines('processed/answers.txt')
    test_questions = read_lines(input_fp, add_root=False)
    print('dataset loaded.')

    tokenizer = Tokenizer()

    ss = SentenceSimilarity(tokenizer)
    ss.set_tokenized_questions(train_tokenized_questions)
    ss.TfidfModel()  # tfidf模型
    print('model initialized.')

    top_15_stream = open('top_15_results.txt', 'w+')

    for i, question in enumerate(test_questions):
        top_15 = ss.similarity(question)

        for similarity, idx in top_15:
            answer = train_answers[idx]
            top_15_stream.write(str(similarity) + '\t' + answer + '\n')
        top_15_stream.write('\n')

        print('top15 in test set: sample -- {}'.format(i))
    top_15_stream.close()


def output_result(input_fp, output_fp):
    predict(input_fp)
    output_stream = open(output_fp, 'w+')
    top_15_lines = read_lines('top_15_results.txt', add_root=False)

    sample_start_index = 0
    while sample_start_index < len(top_15_lines):
        idx = sample_start_index
        line = top_15_lines[idx].strip().split('\t')[1][:-1].replace(",", " ")
        while (re.match("^(\#E\-s\[数字x\])*$", line) or len(line) < 8) \
                and idx - sample_start_index < 14:
            idx += 1
            line = top_15_lines[idx].strip().split('\t')[1][:-1].replace(",", " ")
        output_stream.write(line + '\n')
        sample_start_index += 16  # 根据top的选取数量

    output_stream.close()
