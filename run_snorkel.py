'''
The main class to train the relationship classifier.

This uses a 'DataHandler' class to feed unlabeled training data into the Snorkel framework.
'''


from numpy.random import seed
seed(1234)
from tensorflow import set_random_seed
set_random_seed(5678)

import csv
import pandas as pd
from snorkel.labeling import PandasLFApplier
from snorkel.labeling import LabelModel
from snorkel.utils import probs_to_preds
import embedding.bert as bert
import label_functions
import matplotlib.pyplot as plt
import relation.rels as rel_names
from cui2vec import Cui2Vec
import umls.semantic_types as semantic_types
import data_handler as dh

data_handler = dh.DataHandler()

cui2vec = Cui2Vec().cui2vec

X_gold_sent, X_gold_shortest_path, X_gold_src, X_gold_tgt, X_gold_src_txt, X_gold_tgt_txt, y_gold = data_handler.get_test_data()

X_val_sent, X_val_shortest_path, X_val_src, X_val_tgt, X_val_src_txt, X_val_tgt_txt, y_val = data_handler.get_validation_data()

applier = PandasLFApplier(label_functions.lfs)

df_train = pd.DataFrame(list(zip(*data_handler.get_training_data())), columns=['shortest_path', 'sent', 'src', 'tgt', 'src_txt', 'tgt_txt'])

L_train = applier.apply(df_train)

label_model = LabelModel(cardinality=len(rel_names.rels_txt_to_int), verbose=True)
label_model.fit(L_train, n_epochs=1000, lr=0.01, log_freq=100, seed=123)

label_model.save('./models/LabelModel.model')

train_probs = label_model.predict_proba(L_train)
train_preds = probs_to_preds(train_probs, tie_break_policy='abstain')

df_train = df_train.join(pd.DataFrame({'preds': train_preds, 'probs': list(map(max, train_probs))}))

# -1 to otherwiseRelated
df_train.loc[df_train.preds == -1, 'preds'] = rel_names.rels_txt_to_int['otherwiseRelated']

# Downsample otherwiseRelated
dropNum = len(df_train[df_train.preds == rel_names.rels_txt_to_int['otherwiseRelated']]) - int(df_train['preds'].value_counts().mean())
df_train = df_train.drop(df_train[df_train.preds == rel_names.rels_txt_to_int['otherwiseRelated']].sample(dropNum).index)

cnts = {}
for x in df_train['preds']:
    name = rel_names.rels_int_to_text[x]
    if name not in cnts:
        cnts[name] = 0
    cnts[name] += 1

cnt_rels = [x[0] for x in sorted(cnts.items(), key=lambda x:x[1], reverse=True)]
plt.bar(range(0, len(cnt_rels)), [cnts[x] for x in cnt_rels])
plt.xticks(range(0, len(cnt_rels)), cnt_rels, rotation=90)
plt.show()

for r in cnt_rels:
    print(r, cnts[r])

import rel_models.rel_classifier_clinicalbert as rel_classifier_clinicalbert
from tensorflow.python.keras.utils import to_categorical


with open('./data/weak_label_training.txt', 'w+', encoding='utf8') as f:
    writer = csv.writer(f)
    for x in zip(df_train['sent'], df_train['shortest_path'], df_train['src_txt'], df_train['tgt_txt'], [rel_names.rels_int_to_text[x] for x in df_train['preds']], df_train['probs']):
        writer.writerow(x)

with open('./data/weak_label_training.tsv', 'w+', encoding='utf8') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['sent', 'src', 'tgt', 'label'])
    for x in zip(df_train['sent'], df_train['src_txt'], df_train['tgt_txt'], [rel_names.rels_int_to_text[x] for x in df_train['preds']]):
        writer.writerow(x)

L_test = applier.apply(pd.DataFrame(zip(X_gold_sent, X_gold_shortest_path, X_gold_src, X_gold_tgt), columns=['sent', 'shortest_path', 'src', 'tgt']))

test_probs = label_model.predict_proba(L_test)
test_preds = probs_to_preds(test_probs, tie_break_policy='random')

weak_model_results = rel_classifier_clinicalbert.ClinicalBertClassifier.do_get_accuracy(to_categorical(test_preds, num_classes=rel_names.rels_n),
                                        X_gold_sent,
                                        X_gold_shortest_path,
                                        X_gold_src_txt,
                                        X_gold_tgt_txt,
                                        y_gold,
                                        to_categorical(test_preds, num_classes=rel_names.rels_n))

with open("./output/weak_model_results.csv", 'w+') as f:
    df = pd.DataFrame(weak_model_results).T
    df.to_csv(f, index_label='class')

parameter_scenarios = [
    'all'
]

train_data = (list(df_train['sent']), X_val_sent,
         list(df_train['shortest_path']), X_val_shortest_path,
         list(df_train['src_txt']), X_val_src_txt,
         list(df_train['tgt_txt']), X_val_tgt_txt,
         list(map(cui2vec, list(df_train['src']))), list(map(cui2vec, X_val_src)),
         list(map(cui2vec, list(df_train['tgt']))), list(map(cui2vec, X_val_tgt)),
         list(map(semantic_types.get_sem_type, list(df_train['src']))), list(map(semantic_types.get_sem_type, X_val_src)),
         list(map(semantic_types.get_sem_type, list(df_train['tgt']))), list(map(semantic_types.get_sem_type, X_val_tgt)),
         list(map(semantic_types.get_semantic_group_from_concept, list(df_train['src']))), list(map(semantic_types.get_semantic_group_from_concept, X_val_src)),
         list(map(semantic_types.get_semantic_group_from_concept, list(df_train['tgt']))), list(map(semantic_types.get_semantic_group_from_concept, X_val_tgt)),
         [rel_names.rels_int_to_text[x] for x in df_train['preds']], y_val)


for parameter_scenario in parameter_scenarios:
    if parameter_scenario == 'all':
        nb = rel_classifier_clinicalbert.ClinicalBertClassifier()
    else:
        nb = rel_classifier_clinicalbert.ClinicalBertClassifier(use_features=parameter_scenario)

    nb.train(*train_data)

    model_results = nb.get_accuracy(None,
                                    X_gold_sent,
                                    X_gold_shortest_path,
                                    X_gold_src_txt,
                                    X_gold_tgt_txt,
                                    list(map(cui2vec, X_gold_src)),
                                    list(map(cui2vec, X_gold_tgt)),
                                    list(map(semantic_types.get_sem_type, X_gold_src)),
                                    list(map(semantic_types.get_sem_type, X_gold_tgt)),
                                    list(map(semantic_types.get_semantic_group_from_concept, X_gold_src)),
                                    list(map(semantic_types.get_semantic_group_from_concept, X_gold_tgt)),
                                    y_gold, debug=False)

    print(model_results)

    nb.save()

bert.save()