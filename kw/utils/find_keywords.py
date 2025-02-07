from .preprocessing import lemmatize
from collections import defaultdict 
import pandas as pd
from pprint import pprint
from pathlib import Path



def proccess_kw(words: str):
    words = words.lower()
    words = words.replace(';', '')
    words = words.replace(',', '')
    words = words.replace('.', '')
    words = words.replace('-', ' ')
    words = words.replace('#', ' ')
    words_arr = [word for word in words.split(' ') if len(word) > 1]
    return words_arr






def load_keywords_df(path_to_ds: Path) -> pd.DataFrame:
    df = pd.read_excel(path_to_ds)
    df['keywords'] = df['keywords'].apply(proccess_kw)
    return df



def get_kw2idx(df: pd.DataFrame) -> dict:
    kw2idx = defaultdict(set)
    for idx, row in df.iterrows():
        for word in row['keywords']:
            kw2idx[word].add(idx)
        lemmatize_keywords = lemmatize(' '.join(row['keywords']))
        for word in lemmatize_keywords if lemmatize_keywords is not None else []:
            kw2idx[word].add(idx)
    return kw2idx




def get_topics(words: list, df: pd.DataFrame, kw2idx: dict) -> list:
    # kw2idx = get_kw2idx()
    # pprint(kw2idx)

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
