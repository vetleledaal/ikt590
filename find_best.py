import argparse
import itertools
import os
import subprocess
import tempfile


def run(log_dir, dataset, feature_set):
    fname = f"{dataset}_{'_'.join(feature_set)}"
    fnamelog = f'{fname}.log'
    fnametmp = f'{fname}.tmp.'
    log_file = os.path.join(log_dir, fnamelog)

    if os.path.isfile(log_file):
        return

    with tempfile.NamedTemporaryFile(delete=False, dir=log_dir, prefix=fnametmp) as temp_file:
        cmd = ['python', '-u', 'pipeline.py']
        cmd += ['--dataset', dataset]
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
    datasets = ('FakeNewsNet', 'FakeCovid')
    features = ('text', 'domain')

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    for dataset in datasets:
        for k in range(1, len(features)+1):
            for feature_set in itertools.combinations(features, k):
                run(
                    log_dir=log_dir,
                    dataset=dataset,
                    feature_set=feature_set
                )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--monitor', action='store_true')
    args = parser.parse_args()
    main(args)
