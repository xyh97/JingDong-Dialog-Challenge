# -*- coding: utf-8 -*-
import os
from tfidf.util import remove_file, read_lines, get_path
from tfidf.tokenizer import Tokenizer
import pickle

_CHAT_KEYS = [
    'session_id', 'user_id', 'sent_by_service', 'is_transferred', 'is_repeated', 'sku', 'content']


def process():
    os.makedirs(get_path('processed'), exist_ok=True)
    remove_file('processed/questions.txt')
    remove_file('processed/answers.txt')
    remove_file('processed/tokenized_questions.pkl')

    tokenized_questions = []
    with open(get_path('processed/questions.txt'), 'w+', encoding='utf-8') as q_stream, open(
            get_path('processed/answers.txt'), 'w+', encoding='utf-8') as a_stream:
        tokenizer = Tokenizer()

        question = ''
        answer = ''
        qaqaq = ''
        n_questions = 0
        n_answers = 0
        current_session_id = 'xxxxxxx'  # random session id

        for line in read_lines('data/chat.txt'):
            if not line or line.startswith('会话编号'):
                continue
            line = line.split('\t')
            line = dict(list(zip(_CHAT_KEYS, line)))

            if current_session_id != line['session_id']:
                current_session_id = line['session_id']
                question = ''
                answer = ''
                qaqaq = ''
                n_questions = 0
                n_answers = 0

            if line['sent_by_service'] == '0':
                if n_questions == 3 and n_answers == 2:
                    q_stream.write(qaqaq + '\n')
                    tokenized_questions.append(tokenizer.cut_for_search(qaqaq))
                    a_stream.write(answer + '\n')
                    question = ''
                    answer = ''
                    qaqaq = ''
                    n_questions = 0
                    n_answers = 0

                if answer != '':
                    qaqaq += answer
                    answer = ''
                    n_answers += 1

                question += line['content'] + ','

            elif line['sent_by_service'] == '1':
                if question != '':
                    qaqaq += question
                    question = ''
                    n_questions += 1

                answer = answer + line['content'] + ','

    assert len(read_lines('processed/answers.txt')) == len(read_lines('processed/questions.txt'))
    assert len(read_lines('processed/answers.txt')) == len(tokenized_questions)

    with open(get_path('processed/tokenized_questions.pkl'), 'wb') as f:
        pickle.dump(tokenized_questions, f, -1)


if __name__ == '__main__':
    process()
