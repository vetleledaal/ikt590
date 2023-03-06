import argparse
import glob
import json
import os
import re
import string
from collections import Counter
from time import time
from typing import Dict, List, NamedTuple, Optional

import keras
import nltk
import numpy as np
import pandas as pd
import regex
import tldextract
from keras.preprocessing.text import Tokenizer
from nltk.corpus import stopwords
from scipy.sparse import lil_matrix
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tmu.models.classification.vanilla_classifier import TMClassifier


class TrainTestSet(NamedTuple):
    train_X: np.ndarray
    train_Y: np.ndarray
    test_X: np.ndarray
    test_Y: np.ndarray


# Precompile regular expressions
# Based on https://github.com/yoonkim/CNN_sentence/blob/23e0e1f7355705bb083043fda05c031b15acb38c/process_data.py#L97
RE_NOT_ALNUM = regex.compile(r"[^A-Za-z0-9(),!?'`]")
RE_CONTRACTION = regex.compile(r"'([std]|ve|re|ll)")
RE_PUNCTUATION = regex.compile(r"([(),!?'`])")
RE_WHITESPACE = regex.compile(r"\s{2,}")


def clean_str(text):
    text = RE_NOT_ALNUM.sub(" ", text)
    text = RE_CONTRACTION.sub(" '\\1", text)
    text = RE_PUNCTUATION.sub(" \\1 ", text)
    # TODO: remove stop words here?
    text = RE_WHITESPACE.sub(" ", text)
    return text.strip().lower()


def generate_word_freq(*series: pd.Series, max_n: Optional[int] = None): # TODO: return type
    word_counts = Counter()
    for s in series:
        for row in s:
            cleaned_text = clean_str(row)
            tokens = cleaned_text.split()
            word_counts.update(tokens)
    return word_counts.most_common(max_n)


def generate_word_to_idx(*series: pd.Series, max_n: Optional[int] = None) -> Dict[str, int]:
    word_freq = generate_word_freq(*series, max_n=max_n)
    return {word: idx for idx, (word, _) in enumerate(word_freq)}


def bag_of_words(sentences: pd.Series, word_to_idx: Dict[str, int]):
    # lil_matrix not supported, is flattened in TMU
    # Using np.uint32 as it's the same in TMU
    matrix = np.zeros((len(sentences), len(word_to_idx)), dtype=np.uint32)
    for i, l in enumerate(sentences):
        for w in l:
            if w in word_to_idx:
                matrix[i, word_to_idx[w]] = 1
    return matrix


def train(a: TrainTestSet, metrics: Optional[List[str]] = None):
    # Sanity check
    assert a.train_X.shape[0] == a.train_Y.shape[0]
    assert a.test_X.shape[0] == a.test_Y.shape[0]

    tm = TMClassifier(
        number_of_clauses=args.num_clauses,
        T=args.T,
        s=args.s,
        max_included_literals=32,
        platform=args.device,
        weighted_clauses=True,
        clause_drop_p=0.75
    )

    print(f'[*] Training for {args.epochs} epochs...')
    for i in range(args.epochs):
        t1 = time()
        tm.fit(a.train_X, a.train_Y) # TODO: seed. Uses np.random.shuffle() internally
        t2 = time()

        if metrics is not None:
            test_Y_pred = tm.predict(a.test_X) # TODO: training accuracy/ if the model is training well

            print(f'Epoch {i+1}:', end='')
            if 'acc' in metrics:
                acc = accuracy_score(a.test_Y, test_Y_pred)
                print(f"\tTest Accuracy: {acc:.2%}", end='')
            if 'prec' in metrics:
                prec = precision_score(a.test_Y, test_Y_pred, average='macro')
                print(f"\tTest Precision: {prec:.2%}", end='')
            if 'rec' in metrics:
                rec = recall_score(a.test_Y, test_Y_pred, average='macro')
                print(f"\tTest Recall: {rec:.2%}", end='')
            if 'f1' in metrics:
                f1 = f1_score(a.test_Y, test_Y_pred, average='macro')
                print(f"\tTest F1 score: {f1:.2%}", end='')

        print(f'\tTime: {(t2-t1):.0f}s', end='')
        print('') # explicit newline


'''
For all datasets, if equivalent column exist, use:
text
label
url
tweet_ids
'''

def load_FakeNewsNet():
    dfs = []
    for filename in os.listdir('FakeNewsNet/dataset'):
        if filename.endswith('_real.csv') or filename.endswith('_fake.csv'):
            label = int('_real' in filename)
            df = pd.read_csv(os.path.join('FakeNewsNet/dataset', filename))
            df['label'] = label
            df = df.rename(columns={'title': 'text', 'news_url': 'url'})
            dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

def load_FakeCovid():
    df = pd.read_csv('FakeCovid_July2020.csv')
    df = df.rename(columns={'source_title': 'text', 'article_source': 'url', 'class': 'label'})
    
    # 10 is a magic number
    # TODO: change to min x occurrences
    # why limit?: labels should occur in both train and test (check if sklearn guarantees this)
    labels = Counter(df['label']).most_common(10)
    df = df[df['label'].isin([label[0] for label in labels])]
    return df

def extract_domain(url):
    try:
        return tldextract.extract(url).domain
    except:
        return ''


def encode_df(train_df: pd.DataFrame, test_df: pd.DataFrame) -> TrainTestSet:
    train_X_text = None
    test_X_text = None
    train_X_domain = None
    test_X_domain = None
    train_X_tweet_ids = None
    test_X_tweet_ids = None

    if any(f in args.feature for f in ('all', 'text')):
        print('[*] -> text...')
        word_to_idx_text = generate_word_to_idx(train_df['text'], max_n=args.max_vocab)
        train_X_text = bag_of_words(train_df['text'], word_to_idx_text)
        test_X_text = bag_of_words(test_df['text'], word_to_idx_text)

    if any(f in args.feature for f in ('all', 'domain')):
        if 'url' in train_df.columns and 'url' in test_df.columns:
            print('[*] -> domain...')
            train_df['domain'] = train_df['url'].apply(extract_domain)
            test_df['domain'] = test_df['url'].apply(extract_domain)
            word_to_idx_domain = generate_word_to_idx(train_df['domain'], max_n=args.max_domain)
            train_X_domain = bag_of_words(train_df['domain'], word_to_idx_domain)
            test_X_domain = bag_of_words(test_df['domain'], word_to_idx_domain)

    if any(f in args.feature for f in ('all', 'tweet')):
        if 'tweet_ids' in train_df.columns and 'tweet_ids' in test_df.columns:
            print('[*] -> tweet_ids...')
            word_to_idx_tweet_ids = generate_word_to_idx(train_df['tweet_ids'], max_n=args.max_tweet)
            train_X_tweet_ids = bag_of_words(train_df['tweet_ids'], word_to_idx_tweet_ids)
            test_X_tweet_ids = bag_of_words(test_df['tweet_ids'], word_to_idx_tweet_ids)
    
    print('[*] Encoding complete!') # more or less
    le = LabelEncoder()

    train_X_sub = [x for x in (train_X_text, train_X_domain, train_X_tweet_ids) if x is not None]
    train_X = np.concatenate(train_X_sub, axis=1)
    train_Y = le.fit_transform(train_df['label'])

    test_X_sub = [x for x in (test_X_text, test_X_domain, test_X_tweet_ids) if x is not None]
    test_X = np.concatenate(test_X_sub, axis=1)
    test_Y = le.fit_transform(test_df['label'])

    return TrainTestSet(train_X, train_Y, test_X, test_Y)


def fix_malformed(df: pd.DataFrame) -> pd.DataFrame:
    if args.malformed == 'fix':
        if 'text' in df.columns: df['text'] = df['text'].fillna('')
        if 'url' in df.columns: df['url'] = df['url'].fillna('')
        if 'tweet_ids' in df.columns: df['tweet_ids'] = df['tweet_ids'].fillna('')
    elif args.malformed == 'drop':
        cols_to_drop = [col for col in ('text', 'domain', 'tweet_ids') if col in df.columns]
        if len(cols_to_drop) > 0:
            df = df.dropna(subset=cols_to_drop, how='any')
    return df


def main():
    np.random.seed(args.seed)

    print("[*] Load dataset...")
    if args.dataset == 'FakeNewsNet':
        df = load_FakeNewsNet()
    elif args.dataset == 'FakeCovid':
        df = load_FakeCovid()
    
    print('[*] Fix malformed data...')
    df = fix_malformed(df)

    print("[*] Split...")
    train_df, test_df = train_test_split(df, test_size=args.test_size, random_state=args.seed) # TODO: reuse seed state
    
    print("[*] Encoding...")
    train_test_set = encode_df(train_df, test_df)

    print('='*30)
    print(f'Using {args.device} for training')
    print(f'Dataset: {args.dataset}')
    print(f'TMU params: num-clauses={args.num_clauses}, T={args.T}, s={args.s}')
    print(f'Epochs: {args.epochs}')
    print(f'Feature(s): {args.feature}')
    print(f'max-vocab={args.max_vocab}, max-domain={args.max_domain}, max-tweet={args.max_tweet}')
    print('='*20)
    print(f'Train size: {train_test_set.train_X.shape[0]}')
    print(f'Train classes: {len(set(train_test_set.train_Y))}')
    print(f'Test size: {train_test_set.test_Y.shape[0]}')
    print(f'Test classes: {len(set(train_test_set.test_Y))}')
    print(f'Total features: {train_test_set.train_X.shape[1]}')
    print('='*30)
    train(train_test_set, metrics=('acc', 'prec', 'rec', 'f1'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-clauses', default=5000, type=int) # must be >5000
    parser.add_argument('--T', default=100, type=int) # try 100
    parser.add_argument('--s', default=10.0, type=float) # try 10.0
    parser.add_argument('--epochs', default=100, type=int)
    parser.add_argument('--device', default='GPU', type=str)
    parser.add_argument('--seed', default=42, type=int)
    parser.add_argument('--dataset', choices=('FakeNewsNet', 'FakeCovid'), default='FakeNewsNet')
    parser.add_argument('--feature', choices=('all', 'text', 'domain', 'tweet'), default='all', nargs='+')
    parser.add_argument('--test-size', default=0.2, type=float)
    parser.add_argument('--malformed', choices=('fix', 'drop'), default='fix')
    parser.add_argument('--max-vocab', default=3000, type=int)
    parser.add_argument('--max-domain', default=500, type=int)
    parser.add_argument('--max-tweet', default=500, type=int)
    args = parser.parse_args()
    main()
