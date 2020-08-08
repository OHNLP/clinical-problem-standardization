'''
The main model for classifying relationships between source and target entities.
'''


import string

import numpy as np
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn import metrics
from tensorflow.keras import Model
from tensorflow.keras.backend import set_session
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input, Dropout
from tensorflow.keras.layers import concatenate
from tensorflow.keras.models import load_model
from tensorflow.python.keras.utils import to_categorical

import embedding.bert as bert
import relation.rels as rels
import umls.semantic_types as semantic_types


def configTf():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.50
    config.gpu_options.visible_device_list = "0"
    set_session(tf.Session(config=config))

configTf()

class ClinicalBertClassifier():

    def __init__(self, model=None,
                 use_features=[
                     'shortest_path',
                     'source',
                     'target',
                     'source_vec',
                     'target_vec',
                     'source_sem_type',
                     'target_sem_type',
                     'source_sem_type_group',
                     'target_sem_type_group'
                 ]):
        self.name = "BiLSTMClinicalBert__" + "--".join(sorted(use_features))

        session = tf.Session(graph=tf.Graph())
        with session.graph.as_default():
            tf.compat.v1.keras.backend.set_session(session)

        self.session = session

        if model is not None:
            features = model.split('__')[-1].split(".")[0]
            use_features = features.split("--")

        self.lemmatizer = WordNetLemmatizer()
        self.lemmatizer.lemmatize("warmup") #warmup
        self.stop = set(stopwords.words('english'))
        self.punctuation = set(string.punctuation)

        self.bert_dimensions = 768
        self.cui2vec_dimensions = 500
        self.sem_type_dimensions = len(semantic_types.names)
        self.sem_type_group_dimensions = len(semantic_types.group_names)

        if model is not None:
            with session.graph.as_default():
                self.model = load_model(model)

        self.use_sent = 'sent' in use_features
        self.use_shortest_path = 'shortest_path' in use_features
        self.use_source = 'source' in use_features
        self.use_target = 'target' in use_features
        self.use_source_vec = 'source_vec' in use_features
        self.use_target_vec = 'target_vec' in use_features
        self.use_source_sem_type = 'source_sem_type' in use_features
        self.use_target_sem_type = 'target_sem_type' in use_features
        self.use_source_sem_type_group = 'source_sem_type_group' in use_features
        self.use_target_sem_type_group = 'target_sem_type_group' in use_features

        self.use_features = use_features

    def sentence_to_vec(self, sent):
        return self.sentences_to_vec([sent], persist_embeddings=False)[0]

    def sentences_to_vec(self, sents, persist_embeddings=False):
        sents = [s if s != '' else 'NONE' for s in sents]
        return bert.bert_sent_embeddings(sents, persist=persist_embeddings)

    def build_model(self):
        input_sent = Input(self.bert_dimensions, name="sent")
        input_shortest_path = Input(self.bert_dimensions, name="shortest_path")
        input_source = Input(self.bert_dimensions, name="src_bert_vec")
        input_target = Input(self.bert_dimensions, name="tgt_bert_vec")
        input_source_cui = Input(self.cui2vec_dimensions, name="src_cui_vec")
        input_tgt_cui = Input(self.cui2vec_dimensions, name="tgt_cui_vec")
        input_source_sem_type = Input(self.sem_type_dimensions, name="src_sem_type")
        input_tgt_sem_type = Input(self.sem_type_dimensions, name="tgt_sem_type")
        input_source_sem_type_group = Input(self.sem_type_group_dimensions, name="src_sem_type_group")
        input_tgt_sem_type_group = Input(self.sem_type_group_dimensions, name="tgt_sem_type_group")

        inputs = []
        if self.use_sent: inputs.append(input_sent)
        if self.use_shortest_path: inputs.append(input_shortest_path)
        if self.use_source: inputs.append(input_source)
        if self.use_target: inputs.append(input_target)
        if self.use_source_vec: inputs.append(input_source_cui)
        if self.use_target_vec: inputs.append(input_tgt_cui)
        if self.use_source_sem_type: inputs.append(input_source_sem_type)
        if self.use_target_sem_type: inputs.append(input_tgt_sem_type)
        if self.use_source_sem_type_group: inputs.append(input_source_sem_type_group)
        if self.use_target_sem_type_group: inputs.append(input_tgt_sem_type_group)

        if len(inputs) > 1:
            input = concatenate(inputs)
        else:
            input = inputs[0]

        x = Dropout(0.5)(input)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)

        output = Dense(rels.rels_n, activation='softmax')(x)

        model = Model(inputs, output)

        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

        model.summary()

        return model

    def to_vec(self, hot, dims):
        vec = np.zeros(dims)
        for i in hot:
            vec[i] = 1
        return vec

    def create_X(self, sent, shortest_path, src_txt, tgt_txt, src_vec, tgt_vec, src_sem_type, tgt_sem_type, src_sem_type_group, tgt_sem_type_group):
        X = []

        def sem_type_groups_to_vec(sem_type_groups):
            return np.array(
                [self.to_vec([semantic_types.group_names.index(t) for t in sem_type_group], dims=len(semantic_types.group_names)) for sem_type_group in sem_type_groups])

        def sem_types_to_vec(sem_types):
            return np.array(
                [self.to_vec([semantic_types.names.index(t) if t in semantic_types.names else semantic_types.names.index("NONE")
                              for t in sem_type], dims=len(semantic_types.names)) for sem_type in sem_types])

        if self.use_sent: X.append(np.array(self.sentences_to_vec(sent)))
        if self.use_shortest_path: X.append(np.array(self.sentences_to_vec(shortest_path)))
        if self.use_source: X.append(np.array(self.sentences_to_vec(src_txt)))
        if self.use_target: X.append(np.array(self.sentences_to_vec(tgt_txt)))
        if self.use_source_vec: X.append(np.array(src_vec))
        if self.use_target_vec: X.append(np.array(tgt_vec))
        if self.use_source_sem_type: X.append(sem_types_to_vec(src_sem_type))
        if self.use_target_sem_type: X.append(sem_types_to_vec(tgt_sem_type))
        if self.use_source_sem_type_group: X.append(sem_type_groups_to_vec(src_sem_type_group))
        if self.use_target_sem_type_group: X.append(sem_type_groups_to_vec(tgt_sem_type_group))

        return X

    def predict_probs(self, sent, shortest_path, src_txt, tgt_txt, src_vec, tgt_vec, src_sem_type, tgt_sem_type, src_sem_type_group, tgt_sem_type_group):
        X = self.create_X([sent], [shortest_path], [src_txt], [tgt_txt], [src_vec], [tgt_vec], [src_sem_type], [tgt_sem_type], [src_sem_type_group], [tgt_sem_type_group])

        return self.model.predict(X)[0]

    def predict(self, sent, shortest_path, src_txt, tgt_txt, src_vec, tgt_vec, src_sem_type, tgt_sem_type, src_sem_type_group, tgt_sem_type_group):
        probs = self.predict_probs(sent, shortest_path, src_txt, tgt_txt, src_vec, tgt_vec, src_sem_type, tgt_sem_type, src_sem_type_group, tgt_sem_type_group)
        y_predict = np.argmax(probs)

        return rels.rels_int_to_text[y_predict], probs[y_predict]

    def train(self,
              X_sent, X_sent_v,
              X_shortest_path, X_shortest_path_v,
              X_source, X_source_v,
              X_target, X_target_v,
              X_source_concept, X_source_concept_v,
              X_target_concept, X_target_concept_v,
              X_source_sem_type, X_source_sem_type_v,
              X_target_sem_type, X_target_sem_type_v,
              X_source_sem_type_group, X_source_sem_type_group_v,
              X_target_sem_type_group, X_target_sem_type_group_v,
              y, y_v):
        text_clf = self.build_model()

        X = self.create_X(X_sent,
                          X_shortest_path,
                          X_source,
                          X_target,
                          X_source_concept,
                          X_target_concept,
                          X_source_sem_type,
                          X_target_sem_type,
                          X_source_sem_type_group,
                          X_target_sem_type_group)

        X_val = self.create_X(X_sent_v,
                              X_shortest_path_v,
                              X_source_v,
                              X_target_v,
                              X_source_concept_v,
                              X_target_concept_v,
                              X_source_sem_type_v,
                              X_target_sem_type_v,
                              X_source_sem_type_group_v,
                              X_target_sem_type_group_v)

        y = to_categorical([rels.rels_txt_to_int[rel] for rel in y], num_classes=rels.rels_n)
        y_v = to_categorical([rels.rels_txt_to_int[rel] for rel in y_v], num_classes=rels.rels_n)

        earlystop_cb = EarlyStopping(monitor='val_loss', patience=5, verbose=0, mode='auto')

        text_clf.fit(X, y,
                            validation_data=(X_val, y_v),
                            epochs=100,
                            batch_size=64,
                            verbose=2,
                            callbacks=[earlystop_cb]
                     )

        self.model = text_clf

    def save(self):
        self.model.save('models/' + self.name + '.model')

    def get_accuracy(self, X_weak_labels,
                     X_sent_test,
                     X_shortest_path_test,
                     X_source_test,
                     X_target_test,
                     X_source_concept_test,
                     X_target_concept_test,
                     X_source_sem_type_test,
                     X_target_sem_type_test,
                     X_source_sem_type_group_test,
                     X_target_sem_type_group_test,
                     y_test,
                     debug=False):
        X = self.create_X(X_sent_test,
                          X_shortest_path_test,
                          X_source_test,
                          X_target_test,
                          X_source_concept_test,
                          X_target_concept_test,
                          X_source_sem_type_test,
                          X_target_sem_type_test,
                          X_source_sem_type_group_test,
                          X_target_sem_type_group_test
                          )

        y_predict = self.model.predict(X)

        return self.do_get_accuracy(X_weak_labels, X_sent_test, X_shortest_path_test, X_source_test, X_target_test, y_test, y_predict, debug)


    @staticmethod
    def do_get_accuracy(X_weak_labels, X_sent_test, X_shortest_path_test, X_source_test, X_target_test, y_test, y_predict, debug=False):
        y = to_categorical([rels.rels_txt_to_int[rel] for rel in y_test], num_classes=rels.rels_n)

        used_rels = set.intersection(set(y_test), rels.rels_txt_to_int.keys())

        rel_ints = [rels.rels_txt_to_int[rel] for rel in used_rels]

        def get_results(as_dict):
            return metrics.classification_report(
                np.argmax(y, axis=1),
                np.argmax(y_predict, axis=1),
                labels=rel_ints,
                target_names=[rels.rels_int_to_text[x] for x in rel_ints],
                output_dict=as_dict)

        print(get_results(False))

        if debug:
            for weak_labels, sent, shortest_path, src, tgt, actual, predicted in zip(X_weak_labels, X_sent_test, X_shortest_path_test, X_source_test, X_target_test, y_test, [rels.rels_int_to_text[x] for x in np.argmax(y_predict, axis=1)]):
                if actual != predicted:
                    print(sent)
                    print("\tPath:", shortest_path)
                    print("\tWeak Label:", rels.rels_int_to_text[np.argmax(weak_labels)])
                    print("\tSRC:", src)
                    print("\tTGT:", tgt)
                    print("\tActual:", actual, "Predicted:", predicted)

        labels = [x for x in range(rels.rels_n) if x in rel_ints]
        cm = metrics.confusion_matrix([rels.rels_txt_to_int[x] for x in y_test], np.argmax(y_predict, axis=1), labels=labels)
        print(cm)

        return get_results(True)
