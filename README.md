# IKT590
README may be outdated.

## Setup
```bash
git clone https://github.com/vetleledaal/ikt590.git vetle_ikt590
cd vetle_ikt590
pip install poetry # alternatively use pipx
poetry install --with=dev
```

Note: you need poetry 1.2 or later. Check with `poetry --version`.

If TMU or pycuda fails to install you can check the error in the poetry environment:
```bash
poetry run pip install git+https://github.com/cair/tmu.git
poetry run pip install pycuda
```

### Datasets
You also need to download the datasets (from project root):
```bash
git clone https://github.com/KaiDMML/FakeNewsNet.git
wget https://github.com/Gautamshahi/FakeCovid/raw/master/data/FakeCovid_July2020.csv
```


## How to use
FakeNewsNet supports the features:
- text
- domain
- tweet

FakeCovid support the features:
- text
- domain

Feature permutations:
```
poetry run python pipeline.py --dataset FakeNewsNet --feature all
poetry run python pipeline.py --dataset FakeNewsNet --feature text
poetry run python pipeline.py --dataset FakeNewsNet --feature text domain
poetry run python pipeline.py --dataset FakeNewsNet --feature text domain tweet
poetry run python pipeline.py --dataset FakeNewsNet --feature domain
poetry run python pipeline.py --dataset FakeNewsNet --feature domain tweet
poetry run python pipeline.py --dataset FakeNewsNet --feature tweet

poetry run python pipeline.py --dataset FakeCovid --feature all
poetry run python pipeline.py --dataset FakeCovid --feature text
poetry run python pipeline.py --dataset FakeCovid --feature text domain
poetry run python pipeline.py --dataset FakeCovid --feature domain
```


All arguments:
```
usage: pipeline.py [-h] [--num-clauses NUM_CLAUSES] [--T T] [--s S] [--epochs EPOCHS] [--device DEVICE] [--seed SEED] [--dataset {FakeNewsNet,FakeCovid}]
                   [--feature {all,text,domain,tweet} [{all,text,domain,tweet} ...]] [--test-size TEST_SIZE] [--malformed {fix,drop}] [--max-vocab MAX_VOCAB] [--max-domain MAX_DOMAIN]
                   [--max-tweet MAX_TWEET]

optional arguments:
  -h, --help            show this help message and exit
  --num-clauses NUM_CLAUSES
  --T T
  --s S
  --epochs EPOCHS
  --device DEVICE
  --seed SEED
  --dataset {FakeNewsNet,FakeCovid}
  --feature {all,text,domain,tweet} [{all,text,domain,tweet} ...]
  --test-size TEST_SIZE
  --malformed {fix,drop}
  --max-vocab MAX_VOCAB
  --max-domain MAX_DOMAIN
  --max-tweet MAX_TWEET
```

Defaults:
```
--num-clauses: 5000
--T: 100
--s: 10.0
--epochs: 100
--device: GPU
--seed: 42
--dataset: FakeNewsNet
--feature: all
--test-size: 0.2
--malformed: fix
--max-vocab: 3000
--max-domain: 500
--max-tweet: 500
```


## Possible issues

### ModuleNotFoundError: No module named 'tensorflow'
If you encounter this error on Windows, it may be due to a lack of LongPaths support. You can enable LongPaths by running the following command in an administrative PowerShell terminal:
```ps
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1
```

LongPaths are only supported in Windows 10 Build 1607 or later.

After enabling you could update tensorflow within the poetry environment:
```bash
poetry run pip install tensorflow -U
```

### pycuda fails to install
On Windows, pycuda may fail to install if you don't have the  Microsoft Visual C++ 14.0 or later installed. You can [install "Microsoft Visual C++ Build Tools"](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

On Linux, this is one possible error. No fix yet:
```
pycuda.driver.CompileError: nvcc preprocessing of /tmp/tmp0jmwjg0w.cu failed
[command: nvcc --preprocess -arch sm_52 -I/home/vetle/.cache/pypoetry/virtualenvs/thesis-g87dtkxN-py3.8/lib64/python3.8/site-packages/pycuda/cuda /tmp/tmp0jmwjg0w.cu --compiler-options -P]
[stderr:
b"In file included from /usr/local/cuda-11.2/bin/../targets/x86_64-linux/include/cuda_runtime.h:83,\n                 from <command-line>:\n/usr/local/cuda-11.2/bin/../targets/x86_64-linux/include/crt/host_config.h:139:2: error: #error -- unsupported GNU version! gcc versions later than 10 are not supported! The nvcc flag '-allow-unsupported-compiler' can be used to override this version check; however, using an unsupported host compiler may cause compilation failure or incorrect run time execution. Use at your own risk.\n  139 | #error -- unsupported GNU version! gcc versions later than 10 are not supported! The nvcc flag '-allow-unsupported-compiler' can be used to override this version check; however, using an unsupported host compiler may cause compilation failure or incorrect run time execution. Use at your own risk.\n      |  ^~~~~\n"]
```