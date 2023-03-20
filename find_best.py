import argparse
import itertools
import os
import subprocess
import tempfile
import multiprocessing


def run(log_dir, dataset, T, s, feature_set):
    fname = f"{dataset}_max-vocab=15000_pre=v1_{'_'.join(feature_set)}_T={T}_s={s}"
    fnamelog = f'{fname}.log'
    fnametmp = f'{fname}.tmp.'
    log_file = os.path.join(log_dir, fnamelog)

    if os.path.isfile(log_file):
        return

    with tempfile.NamedTemporaryFile(delete=False, dir=log_dir, prefix=fnametmp) as temp_file:
        cmd = ['python', '-u', 'pipeline.py']
        cmd += ['--dataset', dataset]
        cmd += ['--max-vocab', '15000']
        cmd += ['--T', T]
        cmd += ['--s', s]
        cmd += ['--epochs', '150']
        cmd += ['--feature'] + list(feature_set)

        print(f'$ poetry run {" ".join(cmd)}', flush=True)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in iter(p.stdout.readline, b''):
            if args.monitor:
                print(line.decode('utf-8'), end='', flush=True)
            temp_file.write(line)
            temp_file.flush()

        p.stdout.close()
        p.wait()

    os.rename(temp_file.name, log_file)

def main(args):
    datasets = ('FakeNewsNet-gossipcop', 'FakeNewsNet-politifact')
    features = ('text', 'domain')
    ts = ('50', '150', '200', '250')
    ss = ('5', '10', '15')

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    batch_size = 8

    with multiprocessing.Pool(batch_size) as p:
        for dataset in datasets:
            for k in range(1, len(features)+1):
                for feature_set in itertools.combinations(features, k):
                    for l in range(1, len(ts)+1):
                        for T in itertools.combinations(ts, l):
                            for m in range(1, len(ss)+1):
                                for s in itertools.combinations(ss, m):
                                    p.apply_async(run, kwds={
                                        'log_dir': log_dir,
                                        'dataset': dataset,
                                        'T': T[0],
                                        's': s[0],
                                        'feature_set': feature_set,
                                    })
        p.close()
        p.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--monitor', action='store_true')
    args = parser.parse_args()
    main(args)
