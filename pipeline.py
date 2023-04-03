import pickle
import json
import argparse
import glob
import logging
import os
import string
from collections import Counter
from time import time
from typing import Dict, List, NamedTuple, Optional, Tuple, Union
import sys
import nltk
import numpy as np
import pandas as pd
import regex
import tldextract
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tmu.models.classification.vanilla_classifier import TMClassifier

nltk.download('wordnet')
nltk.download('stopwords')

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # above keras

fname = None

class TrainTestSet(NamedTuple):
    train_x: np.ndarray
    train_y: np.ndarray
    test_x: np.ndarray
    test_y: np.ndarray

noisy_loggers = [
    'tmu.models.classification.vanilla_classifier',
    'tmu.clause_bank.clause_bank_cuda'
]
for logger in noisy_loggers:
    logging.getLogger(logger).setLevel(logging.INFO)


# Precompile regular expressions
# Based on https://github.com/yoonkim/CNN_sentence/blob/23e0e1f7355705bb083043fda05c031b15acb38c/process_data.py#L97
RE_NOT_ALNUM = regex.compile(r'[^A-Za-z0-9(),!?\'`]')
RE_CONTRACTION = regex.compile(r'\'([std]|ve|re|ll)')
RE_PUNCTUATION = regex.compile(r'([(),!?\'`])')
RE_WHITESPACE = regex.compile(r'\s{2,}')

def pre_v1(text):
    text = RE_NOT_ALNUM.sub(' ', text)
    text = RE_CONTRACTION.sub(' \'\\1', text)
    text = RE_PUNCTUATION.sub(' \\1 ', text)
    text = RE_WHITESPACE.sub(' ', text)
    return text.strip().lower().split()


pre_v2_lemmatizer = WordNetLemmatizer()
pre_v2_stop_words = set(nltk.corpus.stopwords.words('english'))
pre_v2_translator = str.maketrans('', '', string.punctuation.replace('\'', ''))
pre_v2_cache = {}

for word in pre_v2_stop_words:
    pre_v2_cache[word] = None

def pre_v2_word(word):
    word = word.lower()
    if word in pre_v2_cache:
        return pre_v2_cache[word]
    result = word.translate(pre_v2_translator).strip('\'')
    result = pre_v2_lemmatizer.lemmatize(result)
    if len(result) < 3 or result.isdigit():
        return None
    pre_v2_cache[word] = result
    return result

def pre_v2(text):
    words = text.split()
    return list(filter(None, map(pre_v2_word, words)))


def pre_tweet_ids(text):
    return [int(num_str) for num_str in text.split()]


def pre_domain(text):
    try:
        return tldextract.extract(text).domain
    except:
        return ''


def token_counter(*series: pd.Series, clean_func, max_n: Optional[int] = None) -> List[Tuple[str, int]]:
    counter = Counter()
    for s in series:
        for row in s:
            tokens = clean_func(row)
            counter.update(tokens)
    return [x for x in counter.most_common(max_n) if x[1] >= 3]

def create_token_index_map(*series: pd.Series, clean_func, max_n: Optional[int] = None) -> Dict[str, int]:
    token_counts = token_counter(*series, clean_func=clean_func, max_n=max_n)
    return {token_count: idx for idx, (token_count, _) in enumerate(token_counts)}


def binary_bag_of_words(token_series: pd.Series, token_index_map: Dict[Union[str, int], int], clean_func):
    token_series = token_series.apply(clean_func)
    matrix = np.zeros((len(token_series), len(token_index_map)), dtype=np.uint32)
    for i, tokens in enumerate(token_series):
        for token in tokens:
            if token in token_index_map:
                matrix[i, token_index_map[token]] = 1
    return matrix


def train(a: TrainTestSet, metrics: Optional[List[str]] = None):
    # Sanity check
    assert a.train_x.shape[0] == a.train_y.shape[0]
    assert a.test_x.shape[0] == a.test_y.shape[0]

    fname_weights = f'{fname}.weights.pkl'
    if os.path.isfile(f'checkpoints/{fname_weights}'):
        with open(f'checkpoints/{fname_weights}', 'rb') as f:
            _, stored_epoch = pickle.load(f)
            if stored_epoch >= args.epochs:
                print(f'[*] The existing checkpoint reached the target epoch ({stored_epoch} >= {args.epochs}), delete this file manually to overwrite. Exiting.')
                sys.exit(1)

    tm = TMClassifier(
        number_of_clauses=args.num_clauses,
        T=args.T,
        s=args.s,
        max_included_literals=args.max_literals, # 8 16 32 64 None, mention in discussion
        platform=args.device,
        weighted_clauses=True,
        clause_drop_p=args.drop_p # experiment with this. 0.25 -> 0.75. mention in discussion
    )

    print(f'[*] Training for {args.epochs} epochs...')
    for i in range(args.epochs):
        time_before = time()
        tm.fit(a.train_x, a.train_y) # TODO: seed. Uses np.random.shuffle() internally
        time_fit = time() - time_before

        if metrics is not None:
            time_before = time()
            train_y_predict = tm.predict(a.train_x)
            time_train_predict = time() - time_before

            time_before = time()
            test_y_predict = tm.predict(a.test_x)
            time_test_predict = time() - time_before

            print(f'Epoch {str(i+1).rjust(3)}: Train%/Test%', end='')
            if 'acc' in metrics:
                accuracy_train = accuracy_score(a.train_y, train_y_predict)
                accuracy_test = accuracy_score(a.test_y, test_y_predict)
                print(f' | Accuracy: {accuracy_train:.2%}/{accuracy_test:.2%}', end='')
            if 'prec' in metrics:
                precision_train = precision_score(a.train_y, train_y_predict, average='macro', zero_division=0)
                precision_test = precision_score(a.test_y, test_y_predict, average='macro', zero_division=0)
                print(f' | Precision: {precision_train:.2%}/{precision_test:.2%}', end='')
            if 'rec' in metrics:
                recall_train = recall_score(a.train_y, train_y_predict, average='macro')
                recall_test = recall_score(a.test_y, test_y_predict, average='macro')
                print(f' | Recall: {recall_train:.2%}/{recall_test:.2%}', end='')
            if 'f1' in metrics:
                f1_train = f1_score(a.train_y, train_y_predict, average='macro')
                f1_test = f1_score(a.test_y, test_y_predict, average='macro')
                print(f' | F1: {f1_train:.2%}/{f1_test:.2%}', end='')

        time_total = time_fit + time_train_predict + time_test_predict
        print(f' | Time: fit={time_fit:03.0f}s, train={time_train_predict:03.0f}s, test={time_test_predict:03.0f}s, total={time_total:03.0f}s')

        with open(f'checkpoints/{fname_weights}', 'wb') as f:
            pickle.dump((fname_weights, i+1), f)




'''
For all datasets, if equivalent column exist, use:
text
label
url
tweet_ids
'''
def load_FakeNewsNet(subset='*'):
    dfs = []
    file_pattern = f'FakeNewsNet/dataset/{subset}_*.csv'
    for filepath in glob.glob(file_pattern):
        filename = os.path.basename(filepath)
        label = int('_real' in filename)
        df = pd.read_csv(filepath)
        df['label'] = label
        df = df.rename(columns={'title': 'text', 'news_url': 'url'})
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

def load_FakeNewsNet_politifact():
    return load_FakeNewsNet('politifact')

def load_FakeNewsNet_gossipcop():
    return load_FakeNewsNet('gossipcop')

def load_FakeCovid():
    df = pd.read_csv('FakeCovid_July2020.csv')
    df = df.rename(columns={'source_title': 'text', 'article_source': 'url', 'class': 'label'})

    # 10 is a magic number
    # TODO: change to min x occurrences
    # why limit?: labels should occur in both train and test (check if sklearn guarantees this)
    labels = Counter(df['label']).most_common(10)
    df = df[df['label'].isin([label[0] for label in labels])]
    return df

def load_HateXPlain(binary=False):
    with open('HateXplain/Data/dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_posts = []
    for post_data in data.values():
        text = ' '.join(post_data['post_tokens'])
        labels = [annotator['target'] for annotator in post_data['annotators'] if 'None' not in annotator['target']]

        if not any(labels):
            label = 'None'
        else:
            label_counts = Counter([label for sublist in labels for label in sublist])

            if len(label_counts) > 1:
                label = 'Multi'
            else:
                label, _ = label_counts.most_common(1)[0]

        if binary:
            label = bool(label != 'None')

        all_posts.append((text, label))
    return pd.DataFrame(all_posts, columns=['text', 'label'])

def load_HateXPlain_binary():
    return load_HateXPlain(binary=True)

def load_fake_news_datasets():
    # Don't actually use this
    dfs = []
    for name, obj in globals().items():
        if name.startswith('load_fake_news_datasets_') and callable(obj):
            dfs.append(obj())
    return pd.concat(dfs)

def load_fake_news_datasets_deception_FakeNewsAMT():
    all_posts = []

    for label in ('fake', 'legit'):
        path = f'fake-news-datasets/datasets/deception_detection_fake_news/data/fakeNewsDataset/{label}/'
        for filename in os.listdir(path):
            with open(path + filename, 'r') as file:
                text = file.read()
                label_value = bool(label == 'fake')
                all_posts.append((text, label_value))

    return pd.DataFrame(all_posts, columns=['text', 'label'])

def load_fake_news_datasets_deception_Celebrity():
    all_posts = []

    for label in ('fake', 'legit'):
        path = f'fake-news-datasets/datasets/deception_detection_fake_news/data/celebrityDataset/{label}/'
        for filename in os.listdir(path):
            with open(path + filename, 'r') as file:
                text = file.read()
                label_value = bool(label == 'fake')
                all_posts.append((text, label_value))

    return pd.DataFrame(all_posts, columns=['text', 'label'])

def load_fake_news_datasets_Election_Day():
    df = pd.read_excel('fake-news-datasets/datasets/electionday_tweets/data/electionday_tweets.xlsx')
    df = df.rename(columns={'is_fake_news': 'label'})
    return df

def load_fake_news_datasets_FakeNewsChallenge():
    df = pd.read_csv('fake-news-datasets/datasets/fake_news_challenge/data/train_stances.csv')
    df = df.rename(columns={'Headline': 'text', 'Stance': 'label'})
    return df

def load_fake_news_datasets_FakeNewsChallenge_body():
    df_bodies = pd.read_csv('fake-news-datasets/datasets/fake_news_challenge/data/train_bodies.csv')
    df_stances = pd.read_csv('fake-news-datasets/datasets/fake_news_challenge/data/train_stances.csv')
    df = pd.merge(df_stances, df_bodies, on='Body ID')
    df = df.rename(columns={'articleBody': 'text', 'Stance': 'label'})
    return df

def load_fake_news_datasets_FakeNewsCorpus():
    df = pd.read_csv('fake-news-datasets/datasets/fake_news_corpus/data/data.csv')
    df = df.rename(columns={'headline': 'text', 'type': 'label'})
    return df

def load_fake_news_datasets_FakeNewsCorpus_body():
    df = pd.read_csv('fake-news-datasets/datasets/fake_news_corpus/data/data.csv')
    df = df.rename(columns={'content': 'text', 'type': 'label'})
    return df


def load_hate_speech_dataset():
    metadata_df = pd.read_csv('hate-speech-dataset/annotations_metadata.csv')

    all_posts = []
    for _, row in metadata_df.iterrows():
        file_id = row['file_id']
        label = bool(row['label'] == 'hate')

        with open(f'hate-speech-dataset/all_files/{file_id}.txt', 'r', encoding='utf-8') as f:
            text = f.read()

        all_posts.append((text, label))
    return  pd.DataFrame(all_posts, columns=['text', 'label'])

def encode_df(train_df: pd.DataFrame, test_df: pd.DataFrame,
    clean_func, features: List[str], max_vocab: int,
    max_domain: int, max_tweet: int) -> TrainTestSet:

    params = {
        'text': {'max_n': max_vocab, 'encoder': clean_func, 'key': 'text'},
        'url': {'max_n': max_domain, 'encoder': pre_domain, 'key': 'domain'},
        'tweet_ids': {'max_n': max_tweet, 'encoder': pre_tweet_ids, 'key': 'tweet'}
    }

    if 'all' not in features:
        params = {k: v for k, v in params.items() if v['key'] in features}

    train_xs = []
    test_xs = []
    for column, values in params.items():
        max_n, encoder, name = values['max_n'], values['encoder'], values['key']

        if all(column in df.columns for df in (train_df, test_df)):
            print(f'[*] Encoding feature: {name}...', end='')

            fname_token_map = f'{fname}.tokens.pkl'
            if os.path.isfile(fname_token_map):
                with open(f'checkpoints/{fname_token_map}', 'rb') as f:
                        token_index_map = pickle.load(f)
            else:
                token_index_map = create_token_index_map(train_df[column], clean_func=encoder, max_n=max_n)
                with open(f'checkpoints/{fname_token_map}', 'wb') as f:
                    pickle.dump(token_index_map, f)

            train_x = binary_bag_of_words(train_df[column], token_index_map, encoder)
            test_x = binary_bag_of_words(test_df[column], token_index_map, encoder)
            print(f' {len(token_index_map)}')

            train_xs.append(train_x)
            test_xs.append(test_x)

        elif name in features:
            print(f'[!] Fatal error, feature {name} was explicitly specified, but not found')
            sys.exit(1)

    train_x = np.concatenate(train_xs, axis=1)
    test_x = np.concatenate(test_xs, axis=1)

    le = LabelEncoder()
    train_y = le.fit_transform(train_df['label'])
    test_y = le.transform(test_df['label'])

    return TrainTestSet(train_x, train_y, test_x, test_y)


def fix_malformed(df: pd.DataFrame) -> pd.DataFrame:
    if args.malformed == 'fix':
        if 'text' in df.columns:
            df['text'] = df['text'].fillna('')
        if 'url' in df.columns:
            df['url'] = df['url'].fillna('')
        if 'tweet_ids' in df.columns:
            df['tweet_ids'] = df['tweet_ids'].fillna('')
    elif args.malformed == 'drop':
        cols_to_drop = [col for col in ('text', 'domain', 'tweet_ids') if col in df.columns]
        if len(cols_to_drop) > 0:
            df = df.dropna(subset=cols_to_drop, how='any')
    return df

dataset_map = {
    'FakeNewsNet': load_FakeNewsNet,
    'FakeNewsNet-politifact': load_FakeNewsNet_politifact,
    'FakeNewsNet-gossipcop': load_FakeNewsNet_gossipcop,
    'FakeCovid': load_FakeCovid,
    'HateXPlain': load_HateXPlain,
    'HateXPlain-binary': load_HateXPlain_binary,
    'fake-news-datasets': load_fake_news_datasets,
    'fake-news-datasets-deception-FakeNewsAMT': load_fake_news_datasets_deception_FakeNewsAMT,
    'fake-news-datasets-deception-Celebrity': load_fake_news_datasets_deception_Celebrity,
    'fake-news-datasets-Election-Day': load_fake_news_datasets_Election_Day,
    'fake-news-datasets-FakeNewsChallenge': load_fake_news_datasets_FakeNewsChallenge,
    'fake-news-datasets-FakeNewsChallenge-body': load_fake_news_datasets_FakeNewsChallenge_body,
    'fake-news-datasets-FakeNewsCorpus': load_fake_news_datasets_FakeNewsCorpus,
    'fake-news-datasets-FakeNewsCorpus-body': load_fake_news_datasets_FakeNewsCorpus_body,
    'hate-speech-dataset': load_hate_speech_dataset,
}

def main(args):
    global fname
    fname = f"{args.dataset}_drop-p={args.drop_p}_max-literals={args.max_literals}_num-clauses={args.num_clauses}_max-vocab={args.max_vocab}_pre={args.preprocessor}_{'_'.join(args.feature)}_T={args.T}_s={args.s}"
    os.makedirs('checkpoints', exist_ok=True)

    np.random.seed(args.seed)

    print('[*] Load dataset...')
    df = dataset_map[args.dataset]()
    assert isinstance(df, pd.DataFrame)

    print('[*] Fix malformed data...')
    df = fix_malformed(df)

    print('[*] Split...')
    train_df, test_df = train_test_split(df, test_size=args.test_size, random_state=args.seed) # TODO: reuse seed state

    print('[*] Encoding...')
    clean_func = pre_v1 if args.preprocessor == 'v1' else pre_v2
    train_test_set = encode_df(
        train_df=train_df,
        test_df=test_df,
        clean_func=clean_func,
        features=args.feature,
        max_vocab=args.max_vocab,
        max_domain=args.max_domain,
        max_tweet=args.max_tweet
    )

    print('='*30)
    print(f'Using {args.device} for training')
    print(f'Dataset: {args.dataset}')
    print(f'TMU params: num-clauses={args.num_clauses}, T={args.T}, s={args.s}')
    print(f'Epochs: {args.epochs}')
    print(f'Feature(s): {", ".join(args.feature)}')
    print(f'max-vocab={args.max_vocab}, max-domain={args.max_domain}, max-tweet={args.max_tweet}')
    print('='*20)
    print(f'Train size: {train_test_set.train_x.shape[0]}')
    print(f'Train classes: {len(set(train_test_set.train_y))}')
    print(f'Test size: {train_test_set.test_y.shape[0]}')
    print(f'Test classes: {len(set(train_test_set.test_y))}')
    print(f'Total features: {train_test_set.train_x.shape[1]}')
    print('='*30)

    if not args.dry:
        train(train_test_set, metrics=('acc', 'prec', 'rec', 'f1'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',  '--num-clauses', default=5000, type=int) # must be >5000
    parser.add_argument('-t',  '--T', default=100, type=int) # step 50
    parser.add_argument('-s',  '--s', default=10.0, type=float) # 5 10 15
    parser.add_argument('-e',  '--epochs', default=100, type=int) # 100 150
    parser.add_argument('-d',  '--device', default='CPU', type=str)
    parser.add_argument('-sd', '--seed', default=42, type=int)
    parser.add_argument('-ds', '--dataset', choices=dataset_map.keys(), default='fake-news-datasets-deception-Celebrity')
    parser.add_argument('-f',  '--feature', choices=('all', 'text', 'domain', 'tweet'), default=('all',), nargs='+')
    parser.add_argument('-ts', '--test-size', default=0.2, type=float)
    parser.add_argument('-m',  '--malformed', choices=('fix', 'drop'), default='fix')
    parser.add_argument('-mv', '--max-vocab', default=3000, type=int) # 15000 (if too slow 10000)
    parser.add_argument('-md', '--max-domain', default=500, type=int)
    parser.add_argument('-mt', '--max-tweet', default=500, type=int)
    parser.add_argument('-p',  '--preprocessor', choices=('v1', 'v2'), default='v1')
    parser.add_argument('-dp',  '--drop-p', default=0.75, type=float)
    parser.add_argument('-ml',  '--max-literals', default=32, type=int)
    parser.add_argument('-dr', '--dry', action='store_true')
    args = parser.parse_args()
    main(args)
