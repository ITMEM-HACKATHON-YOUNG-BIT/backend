from typing import List, Dict
import datetime

import db
from texts import *
import json
import time

from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import pandas as pd
import sklearn
# from sklearn import cross_validation as cv


tokenizer = AutoTokenizer.from_pretrained('cointegrated/rubert-tiny')  # or sberbank-ai/sbert_large_nlu_ru
model = AutoModel.from_pretrained('cointegrated/rubert-tiny')


def get_faq_questions() -> dict:
    return json.load(open('faq.json'))


def get_similar_question_faq(question: str):
    faq_q = get_faq_questions()
    sentences = [question] + list(faq_q.keys())

    tokens = tokenizer(sentences,
                       max_length=128,
                       truncation=True,
                       padding='max_length',
                       return_tensors='pt')
    outputs = model(**tokens)
    embeddings = outputs.last_hidden_state
    mask = tokens['attention_mask'].unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    counted = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / counted
    mean_pooled = mean_pooled.detach().numpy()
    scores = np.zeros((mean_pooled.shape[0], mean_pooled.shape[0]))
    for i in range(mean_pooled.shape[0]):
        scores[i, :] = cosine_similarity(
            [mean_pooled[i]],
            mean_pooled
        )[0]

    answ = list(scores[0][1:])
    for i in range(len(answ)):
        answ[i] = (answ[i], i + 1)

    print(answ)
    sim_q = max(answ)
    print(sim_q)
    if sim_q[0] < .7:
        return None
    return f"{faq_q[sentences[sim_q[1]]]}"


def is_expiring(date: datetime.datetime):
    return (date - datetime.datetime.now()).days < 2


def eq_regions(r1: str, r2: str):
    return True
    # TODO: return r1 == r2


def get_age(birthday: str):
    today = datetime.date.today()
    born = datetime.datetime.strptime(birthday, "%d.%m.%Y").date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred


def pretrain():
    df = pd.read_csv('ml-latest-small/ratings.csv')
    n_users = df['userId'].unique().shape[0]
    n_items = df['eventId'].unique().shape[0]
    input_list = df['eventId'].unique()

    def scale_movie_id(input_id):
        return np.where(input_list == input_id)[0][0] + 1

    df['movieId'] = df['movieId'].apply(scale_movie_id)

    train_data, test_data = sklearn.model_selection.train_test_split(df, train_size=.8)
    train_data_matrix = np.zeros((n_users, n_items))
    for line in train_data.itertuples():
        train_data_matrix[line[1] - 1, line[2] - 1] = line[3]

    test_data_matrix = np.zeros((n_users, n_items))
    for line in test_data.itertuples():
        test_data_matrix[line[1] - 1, line[2] - 1] = line[3]

    user_similarity = sklearn.metrics.pairwise.pairwise_distances(train_data_matrix, metric='cosine')
    item_similarity = sklearn.metrics.pairwise.pairwise_distances(train_data_matrix.T, metric='cosine')

    # item_prediction = predict(train_data_matrix, item_similarity, type='item')
    # user_prediction = predict(train_data_matrix, user_similarity, type='user')


def match(user: dict, event: dict) -> bool:
    if not eq_regions(user['region'], event['region']):
        return False

    if not (event['ageFrom'] <= get_age(user['birthday']) <= event['ageTo']):
        return False

    predict(db.Events.select(), db.Users.select())
    return True


def classification_users_to_events(users: List[Dict], events: List[Dict]):
    result = []
    for event in events:
        result.append({
            'message': EVENT_EXPIRED if is_expiring(event['registrationEndsAt']) else NEW_EVENT,
            'users': []
        })
        result[-1]['message'] = result[-1]['message'] % (event['name'],
                                                         event['organizerName'],
                                                         event['registrationBeginsAt'],
                                                         event['registrationEndsAt'],
                                                         event['beginsAt'],
                                                         event['endsAt'],
                                                         event['minAmount'],
                                                         event['maxAmount'],
                                                         event['url'])
    for user in users:
        for index, event in enumerate(events):
            if match(user, event):
                result[index]['users'].append({
                    'first_name': user['first_name'],
                    'user_tg_id': user['user_tg_id'],
                    'username': user['username_tg']
                })
    return result


def answer_question(question: str):
    return get_similar_question_faq(question)


if __name__ == "__main__":
    print(get_similar_question_faq("?????????? ???????? ?????????????? ????????????, ???????? ?? ???????? ???????????????? ???? ??????????"))
