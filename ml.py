from typing import List, Dict
import datetime
from texts import *
import json
import time

from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np


tokenizer = AutoTokenizer.from_pretrained('cointegrated/rubert-tiny')  # sberbank-ai/sbert_large_nlu_ru
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
    return f"Ваш вопрос похож на '{sentences[sim_q[1]]}'\nОтвет: {faq_q[sentences[sim_q[1]]]}"


def is_expiring(date: datetime.datetime):
    return (date - datetime.datetime.now()).days < 2


def eq_regions(r1: str, r2: str):
    return True
    # TODO: return r1 == r2


def get_age(birthday: str):
    today = datetime.date.today()
    born = datetime.datetime.strptime(birthday, "%d.%m.%Y").date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def match(user: dict, event: dict) -> bool:
    if not eq_regions(user['region'], event['region']):
        return False

    if not (event['ageFrom'] <= get_age(user['birthday']) <= event['ageTo']):
        return False

    # TODO: add ml functions
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
    print(get_similar_question_faq("какие есть статусы заявок, если я хочу податься на грант"))
