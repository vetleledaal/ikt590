# Comparing numbers
## Setup
We are comparing the difference between two different sets of parameters, namely:
```py
# A
max_vocab = '15000'
preprocessor = 'v2'
feature_set = ['text']

T = '150'
s = '10'
num_clauses = '5000'



# B
max_vocab = '15000'
preprocessor = 'v2'
feature_set = ['text']

T = '200' # + 50
s = '15' # + 5
num_clauses = '10000' # + 5000
```

## Metrics @ Epoch 150
| Model                                     | A accuracy | B accuracy | &#8710;% accuracy | A precision | B precision | &#8710;% precision | A recall | B recall | &#8710;% recall | A F1   | B F1   | &#8710;% F1 |
| :---------------------------------------- | :--------- | :--------- | :---------------- | :---------- | :---------- | :----------------- | :------- | :------- | :-------------- | :----- | :----- | :---------- |
| FakeNewsNet                               |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| FakeNewsNet-politifact                    | 0.7594     | 0.7217     | -4.96%            | 0.7518      | 0.7453      | -0.86%             | 0.7695   | 0.7584   | -1.44%          | 0.7527 | 0.7206 | -4.26%      |
| FakeNewsNet-gossipcop                     |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| FakeCovid                                 |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| HateXPlain                                | 0.4161     | 0.4104     | -1.36%            | 0.3214      | 0.3198      | -0.49%             | 0.5286   | 0.4823   | -8.75%          | 0.3672 | 0.3593 | -2.15%      |
| HateXPlain-binary                         |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| fake-news-datasets                        |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| fake-news-datasets-deception-FakeNewsAMT  | 0.4745     | 0.5000     | 5.37%             | 0.4745      | 0.4970      | 4.74%              | 0.4763   | 0.4972   | 4.38%           | 0.4678 | 0.4891 | 4.55%       |
| fake-news-datasets-deception-Celebrity    | 0.7000     | 0.7300     | 4.28%             | 0.6981      | 0.7325      | 4.92%              | 0.6965   | 0.7226   | 3.74%           | 0.6970 | 0.7238 | 3.84%       |
| fake-news-datasets-Election-Day           | 0.8534     | 0.8759     | 2.63%             | 0.6341      | 0.6682      | 5.37%              | 0.6720   | 0.6846   | 1.87%           | 0.6489 | 0.6758 | 4.14%       |
| fake-news-datasets-FakeNewsChallenge      |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| fake-news-datasets-FakeNewsChallenge-body |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| fake-news-datasets-FakeNewsCorpus         |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| fake-news-datasets-FakeNewsCorpus-body    |            |            |                   |             |             |                    |          |          |                 |        |        |             |
| hate-speech-dataset                       | 0.6117     | 0.7168     | 17.18%            | 0.5833      | 0.5974      | 2.41%              | 0.7246   | 0.7359   | 1.55%           | 0.5218 | 0.5870 | 12.49%      |


## Other metrics from papers
| Model                                    | Accuracy | Precision | Recall | F1    |
| :--------------------------------------- | :------- | :-------- | :----- | :---- |
| FakeNewsNet-politifact                   |          |           |        |       |
| HateXPlain*                              | 0.698    |           |        | 0.687 |
| fake-news-datasets-deception-FakeNewsAMT | 0.500    |           |        |       |
| fake-news-datasets-deception-Celebrity   | 0.640    |           |        |       |
| fake-news-datasets-Election-Day          | -        | -         | -      | -     |
| hate-speech-dataset                      | 0.730    |           |        |       |

Note: significant numbers not preserved\
\* Likely different preprocessing


## Other hyper-parameters
| Model (Using B)                            | p=.25 acc | p=.75 acc | p=.25 prec | p=.75 prec | p=.25 rec | p=.75 rec | p=.25 f1 | p=.75 f1 |
| :----------------------------------------- | :-------- | :-------- | :--------- | :--------- | :-------- | :-------- | :------- | :------- |
| fake-news-datasets-Election-Day            | 0.7782    | 0.8759    | 0.5978     | 0.6682     | 0.6959    | 0.6846    | 0.6089   | 0.6758   |
| fake-news-datasets-deception-FakeNewsAMT** | 0.4688    | 0.5000    | 0.4639     | 0.4970     | 0.4661    | 0.4972    | 0.4588   | 0.4891   |
| fake-news-datasets-deception-Celebrity**   | 0.7200    | 0.7300    | 0.7182     | 0.7325     | 0.7182    | 0.7226    | 0.7182   | 0.7238   |


| Model (Using A)                                            | Accuracy | Precision | Recall | F1     |
| :--------------------------------------------------------- | :------- | :-------- | :----- | :----- |
| fake-news-datasets-Election-Day max-literals=3             | 0.7932   | 0.6005    | 0.6878 | 0.6149 |
| fake-news-datasets-Election-Day max-literals=8             | 0.8346   | 0.6198    | 0.6780 | 0.6381 |
| fake-news-datasets-Election-Day max-literals=16            | 0.8459   | 0.6104    | 0.6350 | 0.6204 |
| fake-news-datasets-Election-Day max-literals=32            | 0.8459   | 0.6250    | 0.6678 | 0.6407 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=3**  | 0.5104   | 0.5081    | 0.5074 | 0.4982 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=8**  | 0.4583   | 0.4559    | 0.4568 | 0.4545 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=16** | 0.4896   | 0.4881    | 0.4883 | 0.4869 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=32** | 0.5312   | 0.5308    | 0.5282 | 0.5195 |
| fake-news-datasets-deception-Celebrity max-literals=3**    | 0.7600   | 0.7657    | 0.7520 | 0.7537 |
| fake-news-datasets-deception-Celebrity max-literals=8**    | 0.7300   | 0.7303    | 0.7242 | 0.7254 |
| fake-news-datasets-deception-Celebrity max-literals=16**   | 0.7300   | 0.7355    | 0.7210 | 0.7220 |
| fake-news-datasets-deception-Celebrity max-literals=32**   | 0.7200   | 0.7208    | 0.7134 | 0.7144 |

| Model (Using B)                                            | Accuracy | Precision | Recall | F1     |
| :--------------------------------------------------------- | :------- | :-------- | :----- | :----- |
| fake-news-datasets-Election-Day max-literals=3             | 0.8346   | 0.6198    | 0.6780 | 0.6381 |
| fake-news-datasets-Election-Day max-literals=8             | 0.8459   | 0.6315    | 0.6843 | 0.6499 |
| fake-news-datasets-Election-Day max-literals=16            | 0.8496   | 0.6294    | 0.6699 | 0.6448 |
| fake-news-datasets-Election-Day max-literals=32            | 0.8835   | 0.6677    | 0.6395 | 0.6516 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=3**  | 0.4062   | 0.4034    | 0.4049 | 0.4031 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=8**  | 0.4688   | 0.4651    | 0.4666 | 0.4617 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=16** | 0.4062   | 0.4034    | 0.4049 | 0.4031 |
| fake-news-datasets-deception-FakeNewsAMT max-literals=32** | 0.4271   | 0.4215    | 0.4249 | 0.4195 |
| fake-news-datasets-deception-Celebrity max-literals=3**    | 0.7300   | 0.7447    | 0.7178 | 0.7175 |
| fake-news-datasets-deception-Celebrity max-literals=8**    | 0.7400   | 0.7397    | 0.7351 | 0.7362 |
| fake-news-datasets-deception-Celebrity max-literals=16**   | 0.7200   | 0.7233    | 0.7118 | 0.7126 |
| fake-news-datasets-deception-Celebrity max-literals=32**   | 0.7200   | 0.7208    | 0.7134 | 0.7144 |

\*\* Overfitted (100% +- 2% accuracy on train data)


