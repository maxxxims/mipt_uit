from .preprocessing import lemmatize
from collections import defaultdict 
import pandas as pd


def proccess_kw(words: str):
    words = words.lower()
    words = words.replace(';', '')
    words = words.replace(',', '')
    words = words.replace('.', '')
    words = words.replace('-', ' ')

    words_arr = [word for word in words.split(' ') if len(word) > 1]

    return words_arr


df = pd.read_excel('kw/data/keywords.xlsx')
df['keywords'] = df['keywords'].apply(proccess_kw)



def get_kw2idx() -> dict:
    kw2idx = defaultdict(set)
    for idx, row in df.iterrows():
        for word in row['keywords']:
            kw2idx[word].add(idx)

        # print(row['keywords'])
        # print(lemmatize(' '.join(row['keywords'])))

        lemmatize_keywords = lemmatize(' '.join(row['keywords']))
        for word in lemmatize_keywords if lemmatize_keywords is not None else []:
            kw2idx[word].add(idx)
    return kw2idx



def get_topics(words: list) -> list:
    kw2idx = get_kw2idx()
    # print(kw2idx)
    topics = []
    unique_topic_names = []
    for word in words:
        topics_indexes = kw2idx[word]
        for idx in topics_indexes:
            row = df.loc[idx]
            name = str(row['name']) 
            if name not in unique_topic_names:
                unique_topic_names.append(name)
                found_topic = {
                    'name': name,
                    'top_kb_index': int(row['top_kb_index']),
                    'second_kb_index': int(row['second_kb_index']),
                    'third_kb_index': int(row['third_kb_index']) if pd.notnull(row['third_kb_index']) else -1
                }
                topics.append(found_topic)

    return topics


if __name__ == "__main__":
    #t = get_topics(words=['мои', 'документы', 'мфти', 'мой', 'документ'])
    #print(t)
    #sorted_dict = sorted(t.items(), reverse=False)
    #t2 = sorted(t, key=lambda el: -t[el])
    words=['мои', 'документы', 'мфти', 'мой', 'документ']
    kw2idx = get_kw2idx()
    # topics = defaultdict(int)
    topics = []
    for word in words:
        topics_indexes = kw2idx[word]
        for idx in topics_indexes:
            row = df.loc[idx]
            found_topic = {
                'name': row['name'],
                'top_kb_index': row['top_kb_index'],
                'second_kb_index': row['second_kb_index'],
                'third_kb_index': row['third_kb_index'] if pd.notnull(row['third_kb_index']) else None
            }
            #print(f"third = {row['third_kb_index']}, {pd.notnull(row['third_kb_index'])}")
            topics.append(found_topic)
    print(topics)