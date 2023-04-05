# CZ4034 Group10 Project
Repo of CZ4034 IR Group10 Project

## Data Collection
**'1_crawling' folder**
1. scrape_tweets.ipynb
2. explore_data.ipynb

## Data Preprocessing
**'2_preprocesing' folder**
1. preprocess_tweets.ipynb
2. prepare_files.ipynb
3. preprocessing_experiments.ipynb

## Data Augmentation
**'3_augmentation' folder**
1. augmentation_experiments.ipynb
2. augment_train.ipynb

## Indexing
**'4_indexing' folder**


## Sentiment Analysis
**'5_classification" folder**
1. unsupervised_classifiers.ipynb
2. xgboost_classifier.ipynb
3. lightgbm_classifier.ipynb
4. knn_classifier.ipynb
5. svm_classifier.ipynb
6. decisiontree_classifier.ipynb
7. naivebayes_classifier.ipynb
8. majority_voting.ipynb
9. lstm_classifier.ipynb
10. bert_classifier.ipynb
11. final_results.csv

## User Interface
**'6_ui" folder**
__How To Run__
* `cd 6_ui`
* `python3 -m venv env` (mac) or `python -m venv env` (windows)
* `source env/bin/activate` (mac) or `env\Scripts\activate` (windows)
* `pip install -r requirements.txt`
* `pip install streamlit`
* `streamlit run hello.py`

__How deactivate virtual environment__
* `deactivate`

__TODO__
* put back lemmatizer
* remove debugging stuff `st.write()`
* remove dummy pages `hello.py` and `1_plot.py`
* integrate with indexing
* update `requirements.txt`

## Datasets
**'datasets' folder**
1. label_dataset_final.csv
2. full_dataset_final.csv
3. train_aug.csv
4. test.csv