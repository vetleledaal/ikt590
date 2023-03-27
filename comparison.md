# Comparing numbers
## Summary
|                | PolitiFact Acc | GossipCop Acc |
| :------------- | :------------- | :------------ |
| Paper 1 (TBA)  | 0.8632**       | 0.8388**      |
| Paper 2 (2019) | 0.691          | 0.822         |
| Paper 3 (2020) | 0.8            | 0.82          |
| Paper 4 (2023) | 0.584          | -             |
| Paper 5 (2020) | 0.846          | 0.86          |
| Paper 6 (2021) | 0.9156*        | 0.9156*       |

\* Combined dataset.\
\*\* Not updated below. (FakeNewsNet-politifact_max-vocab=15000_pre=v2_text_domain_T=200_s=15 and FakeNewsNet-gossipcop_max-vocab=15000_pre=v2_domain_T=250_s=5)


## Paper 1: This paper
<table>
    <tr>
        <th rowspan="2">Model</th>
        <th colspan="4" style="text-align: center">PolitiFact</th>
        <th colspan="4" style="text-align: center">GossipCop</td>
        <th colspan="4" style="text-align: center">PolitiFact+GossipCop</td>
    </tr>
    <tr>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
    </tr>
    <tr>
        <td>TM+Text</td>
        <td>0.750</td>
        <td>0.742</td>
        <td>0.761</td>
        <td>0.743</td>
        <td>0.778</td>
        <td>0.695</td>
        <td>0.743</td>
        <td>0.693</td>
        <td>0.742</td>
        <td>0.686</td>
        <td>0.740</td>
        <td>0.694</td>
    </tr>
    <tr>
        <td>TM+Domain</td>
        <td>0.768</td>
        <td style="font-weight: bold">0.849</td>
        <td>0.779</td>
        <td>0.762</td>
        <td>0.732</td>
        <td>0.666</td>
        <td>0.708</td>
        <td>0.675</td>
        <td>0.734</td>
        <td>0.672</td>
        <td>0.714</td>
        <td>0.681</td>
    </tr>
    <tr>
        <td>TM+Text+Domain</td>
        <td>0.764</td>
        <td>0.754</td>
        <td>0.770</td>
        <td>0.756</td>
        <td style="font-weight: bold">0.809</td>
        <td style="font-weight: bold">0.739</td>
        <td style="font-weight: bold">0.775</td>
        <td style="font-weight: bold">0.744</td>
        <td style="font-weight: bold">0.782</td>
        <td style="font-weight: bold">0.721</td>
        <td style="font-weight: bold">0.766</td>
        <td style="font-weight: bold">0.734</td>
    </tr>
    <tr>
        <td>TM+Tweet</td>
        <td>0.632</td>
        <td>0.688</td>
        <td>0.514</td>
        <td>0.387</td>
        <td>0.241</td>
        <td>0.121</td>
        <td>0.500</td>
        <td>0.194</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>TM+Tweet+Text</td>
        <td>0.774</td>
        <td>0.764</td>
        <td>0.781</td>
        <td>0.766</td>
        <td>0.799</td>
        <td>0.724</td>
        <td>0.737</td>
        <td>0.716</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>TM+Tweet+Domain</td>
        <td>0.750</td>
        <td>0.840</td>
        <td>0.764</td>
        <td>0.745</td>
        <td>0.749</td>
        <td>0.672</td>
        <td>0.702</td>
        <td>0.681</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>TM+Tweet+Text+Domain</td>
        <td style="font-weight: bold">0.788</td>
        <td>0.776</td>
        <td style="font-weight: bold">0.792</td>
        <td style="font-weight: bold">0.780</td>
        <td>0.788</td>
        <td>0.724</td>
        <td>0.771</td>
        <td>0.738</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
</table>

### Method
* 80/20 split
* Tokenize
* Convert text to lowercase
* Convert text to a binary bag-of-words vector

### Size
* PolitiFact has a total of 1056
* GossipCop has a total of 22140

## Paper 2: FakeNewsNet: A Data Repository with News Content, Social Context and Dynamic Information for Studying Fake News on Social Media (2019)
[PDF](https://www.researchgate.net/profile/Suhang-Wang/publication/327464821_FakeNewsNet_A_Data_Repository_with_News_Content_Social_Context_and_Dynamic_Information_for_Studying_Fake_News_on_Social_Media/links/5b97152e299bf14739440f89/FakeNewsNet-A-Data-Repository-with-News-Content-Social-Context-and-Dynamic-Information-for-Studying-Fake-News-on-Social-Media.pdf)

<table>
    <tr>
        <th rowspan="2">Model</th>
        <th colspan="4" style="text-align: center">PolitiFact</th>
        <th colspan="4" style="text-align: center">GossipCop</td>
    </tr>
    <tr>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
    </tr>
    <tr>
        <td>SVM</td>
        <td>0.580</td>
        <td>0.611</td>
        <td>0.717</td>
        <td>0.659</td>
        <td>0.470</td>
        <td>0.462</td>
        <td>0.451</td>
        <td>0.456</td>
    </tr>
    <tr>
        <td>Logic regression</td>
        <td>0.642</td>
        <td>0.757</td>
        <td>0.543</td>
        <td>0.633</td>
        <td style="font-weight: bold">0.822</td>
        <td style="font-weight: bold">0.897</td>
        <td>0.722</td>
        <td style="font-weight: bold">0.799</td>
    </tr>
    <tr>
        <td>Naive Bayes</td>
        <td>0.617</td>
        <td>0.674</td>
        <td>0.630</td>
        <td>0.651</td>
        <td>0.704</td>
        <td>0.735</td>
        <td style="font-weight: bold">0.765</td>
        <td>0.798</td>
    </tr>
    <tr>
        <td>CNN</td>
        <td>0.629</td>
        <td style="font-weight: bold">0.807</td>
        <td>0.456</td>
        <td>0.583</td>
        <td>0.703</td>
        <td>0.789</td>
        <td>0.623</td>
        <td>0.699</td>
    </tr>
    <tr>
        <td>Social Article Fusion /S</td>
        <td>0.654</td>
        <td>0.600</td>
        <td>0.789</td>
        <td>0.681</td>
        <td>0.741</td>
        <td>0.709</td>
        <td>0.761</td>
        <td>0.734</td>
    </tr>
    <tr>
        <td>Social Article Fusion /A</td>
        <td>0.667</td>
        <td>0.667</td>
        <td>0.579</td>
        <td>0.619</td>
        <td>0.796</td>
        <td>0.782</td>
        <td>0.743</td>
        <td>0.762</td>
    </tr>
    <tr>
        <td>Social Article Fusion</td>
        <td style="font-weight: bold">0.691</td>
        <td>0.638</td>
        <td style="font-weight: bold">0.789</td>
        <td style="font-weight: bold">0.706</td>
        <td>0.796</td>
        <td>0.820</td>
        <td>0.753</td>
        <td>0.785</td>
    </tr>
</table>

### Method
* 80/20 split
* Unknown or "default" settings

### Size
* PolitiFact has a total of 1056 (624 real, 432 fake)
* GossipCop has a total of 22865 (16817 real, 6048 fake)

## Paper 3: Exploring N-gram, Word Embedding and Topic Models for Content-based Fake News Detection in FakeNewsNet Evaluation (2020)
[PDF](https://www.researchgate.net/profile/Oluwafemi-Oriola-3/publication/342988089_ISSN_2249-0868_Foundation_of_Computer_Science_FCS/links/5f1075d845851512999ebf86/ISSN2249-0868-Foundation-of-Computer-Science-FCS.pdf)

<table>
    <tr>
        <th rowspan="2">Model</th>
        <th colspan="4" style="text-align: center">PolitiFact</th>
        <th colspan="4" style="text-align: center">GossipCop</td>
    </tr>
    <tr>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
    </tr>
    <tr>
        <td>LogReg</td>
        <td>0.64</td>
        <td>0.76</td>
        <td>0.54</td>
        <td>0.63</td>
        <td style="font-weight: bold">0.82</td>
        <td style="font-weight: bold">0.90</td>
        <td>0.72</td>
        <td style="font-weight: bold">0.80</td>
    </tr>
    <tr>
        <td>Social Article Fusion</td>
        <td>0.69</td>
        <td>0.64</td>
        <td style="font-weight: bold">0.79</td>
        <td>0.71</td>
        <td>0.80</td>
        <td>0.82</td>
        <td>0.75</td>
        <td>0.79</td>
    </tr>
    <tr>
        <td>N-gram</td>
        <td style="font-weight: bold">0.80</td>
        <td style="font-weight: bold">0.79</td>
        <td>0.78</td>
        <td style="font-weight: bold">0.78</td>
        <td style="font-weight: bold">0.82</td>
        <td>0.75</td>
        <td style="font-weight: bold">0.79</td>
        <td>0.77</td>
    </tr>
    <tr>
        <td>Topic</td>
        <td>0.60</td>
        <td>0.55</td>
        <td>0.53</td>
        <td>0.51</td>
        <td>0.51</td>
        <td>0.51</td>
        <td>0.51</td>
        <td>0.47</td>
    </tr>
    <tr>
        <td>Word2Vec</td>
        <td>0.73</td>
        <td>0.73</td>
        <td>0.74</td>
        <td>0.73</td>
        <td>0.78</td>
        <td>0.71</td>
        <td>0.76</td>
        <td>0.72</td>
    </tr>
    <tr>
        <td>N-gram + Topic</td>
        <td>0.77</td>
        <td>0.76</td>
        <td>0.76</td>
        <td>0.76</td>
        <td>0.82</td>
        <td>0.75</td>
        <td>0.78</td>
        <td>0.76</td>
    </tr>
    <tr>
        <td>N-gram + Word2Vec</td>
        <td>0.72</td>
        <td>0.72</td>
        <td>0.73</td>
        <td>0.72</td>
        <td>0.78</td>
        <td>0.71</td>
        <td>0.76</td>
        <td>0.72</td>
    </tr>
    <tr>
        <td>Topic + Word2Vec</td>
        <td>0.42</td>
        <td>0.49</td>
        <td>0.49</td>
        <td>0.39</td>
        <td>0.63</td>
        <td>0.60</td>
        <td>0.64</td>
        <td>0.60</td>
    </tr>
    <tr>
        <td>N-gram + Topic + Word2Vec</td>
        <td>0.40</td>
        <td>0.45</td>
        <td>0.48</td>
        <td>0.36</td>
        <td>0.58</td>
        <td>0.57</td>
        <td>0.60</td>
        <td>0.54</td>
    </tr>
</table>

### Method
* 80/20 split
* Tokenize
* Stemming
* Remove duplicates
* Remove punctuation
* Remove special characters and symbols
* Remove hash from hashtags
* Remove stop words
* Convert text to lowercase

### Size
After preprocessing:
* PolitiFact has a total of 968 (426 real, 542 fake)
* GossipCop has a total of 20796 (4804 real, 15965 fake)

## Paper 4: Machine Learning vs Deep Learning Models for Detecting Fake News: A Comparative Analysis on Fake-NewsNet Dataset (2023)
[PDF](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4382241)

Note: this is an aggregate of the presented data.
<table>
    <tr>
        <th rowspan="2">Model</th>
        <th colspan="4" style="text-align: center">PolitiFact</th>
    </tr>
    <tr>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
    </tr>
    <tr>
        <td>NB</td>
        <td style="font-weight: bold">0.584</td>
        <td style="font-weight: bold">0.585</td>
        <td>0.565</td>
        <td>0.545</td>
    </tr>
    <tr>
        <td>SVM</td>
        <td>0.574</td>
        <td>0.645</td>
        <td>0.575</td>
        <td>0.515</td>
    </tr>
    <tr>
        <td>LSTM</td>
        <td>0.560</td>
        <td>0.570</td>
        <td style="font-weight: bold">0.580</td>
        <td style="font-weight: bold">0.555</td>
    </tr>
</table>

### Method
* 80/10/10 split
* Tokenize
* Stemming
* "Clean" punctuation
* Remove some punctuation
* Remove stop words
* Remove numbers
* Drop invalid data
* Convert text to lowercase
* Convert text to TF-IDF

### Size
* PolitiFact has a total of 1056 (624 real, 432 fake)


## Paper 5: SpotFake+: A Multimodal Framework for Fake News Detection via Transfer Learning (Student Abstract) (2020)
[PDF](https://ojs.aaai.org/index.php/AAAI/article/download/7230/7084)
[GitHub](https://github.com/shiivangii/SpotFakePlus)

### Text
<table>
    <tr>
        <th rowspan="2">Model</th>
        <th style="text-align: center">PolitiFact</th>
        <th style="text-align: center">GossipCop</th>
    </tr>
    <tr>
        <th>Acc</th>
        <th>Acc</th>
    </tr>
    <tr>
        <td>SVM</td>
        <td>0.58</td>
        <td>0.497</td>
    </tr>
    <tr>
        <td>Logistic Regression</td>
        <td>0.642</td>
        <td>0.648</td>
    </tr>
    <tr>
        <td>Naive Bayes</td>
        <td>0.617</td>
        <td>0.624</td>
    </tr>
    <tr>
        <td>CNN</td>
        <td>0.629</td>
        <td>0.723</td>
    </tr>
    <tr>
        <td>SAF (Social Article Fusion)</td>
        <td>0.691</td>
        <td>0.689</td>
    </tr>
    <tr>
        <td>XLNet + dense layer</td>
        <td style="font-weight: bold">0.74</td>
        <td>0.836</td>
    </tr>
    <tr>
        <td>XLNet + CNN</td>
        <td>0.721</td>
        <td style="font-weight: bold">0.84</td>
    </tr>
    <tr>
        <td>XLNet + LSTM</td>
        <td>0.721</td>
        <td>0.807</td>
    </tr>
</table>

### Text + Image
<table>
    <tr>
        <th rowspan="2">Model</th>
        <th style="text-align: center">PolitiFact</th>
        <th style="text-align: center">GossipCop</th>
    </tr>
    <tr>
        <th>Acc</th>
        <th>Acc</th>
    </tr>
    <tr>
        <td>EANN</td>
        <td>0.74</td>
        <td style="font-weight: bold">0.86</td>
    </tr>
    <tr>
        <td>MVAE</td>
        <td>0.673</td>
        <td>0.775</td>
    </tr>
    <tr>
        <td>SpotFake</td>
        <td>0.721</td>
        <td>0.807</td>
    </tr>
    <tr>
        <td>SpotFake+</td>
        <td style="font-weight: bold">0.846</td>
        <td>0.856</td>
    </tr>
</table>

### Method
* Remove logos
* Drop samples without images

### Size
Before preprocessing:
* PolitiFact has a total of 1056 (624 real, 432 fake)
* GossipCop has a total of 22140 (16817 real, 5323 fake)

After preprocessing:
* PolitiFact has a total of 485 (321 real, 164 fake)
* GossipCop has a total of 12840 (10259 real, 2581 fake)

### Paper 6: A Heuristic-driven Uncertainty based Ensemble Framework for Fake News Detection in Tweets and News Articles (2021)
[PDF](https://arxiv.org/pdf/2104.01791.pdf)

<table>
    <tr>
        <th rowspan="2">Model</th>
        <th colspan="4" style="text-align: center">PolitiFact + GossipCop</th>
    </tr>
    <tr>
        <th>Acc</th>
        <th>Prec</th>
        <th>Rec</th>
        <th>F1</th>
    </tr>
    <tr>
        <td>FakeFlow</td>
        <td>0.82</td>
        <td>0.82</td>
        <td>0.82</td>
        <td>0.82</td>
    </tr>
    <tr>
        <td>One-Hot LR</td>
        <td>0.7670</td>
        <td>0.7670</td>
        <td>0.7670</td>
        <td>0.7670</td>
    </tr>
    <tr>
        <td>FakeNewsTracker</td>
        <td>0.7186</td>
        <td>0.7186</td>
        <td>0.7186</td>
        <td>0.7186</td>
    </tr>
    <tr>
        <td>Ensemble Model + Heuristic Post-Processing</td>
        <td>0.9007</td>
        <td>0.9007</td>
        <td>0.9007</td>
        <td>0.9007</td>
    </tr>
    <tr>
        <td>SFFN (with MCDropout) + Heuristic Post-Processing</td>
        <td style="font-weight: bold">0.9156</td>
        <td style="font-weight: bold">0.9156</td>
        <td style="font-weight: bold">0.9156</td>
        <td style="font-weight: bold">0.9156</td>
    </tr>
</table>

### Method
* 80/10/10 split
* For tweets tweet-preprocessor was used (a Python package) to filter out usernames, URLs, emojis, etc.
* For articles, filter out: usernames, URLs from Instagram, Facebook, Twitter, etc.
* Different tokenizers (from huggingface)
* Vocabulary trained on a large corpus like GLUE, wikitext-103, CommonCrawl, etc.
* Transfer learning
* News body was crawled
* Ensemble of models used for balancing
*

### Size
* PolitiFact has a total of 1056 (624 real, 432 fake)
* GossipCop has a total of 22140 (16817 real, 5323 fake)

Data was augmented by crawling "E! online", PolitiFact, and GossipCop.

After crawling:
* PolitiFact has a total of 1011 (610 real, 401 fake)
* GossipCop has a total of 20474 (15151 real, 5323 fake)