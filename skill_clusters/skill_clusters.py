# encoding: utf-8
"""
skill_clusters.py
"""
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


class SkillClusters():

    def load_data(self, filename):
        df = pd.read_csv(filename, index_col=False)
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df['name'] = df['name'].apply(lambda x: x.lower())
        word_list = df['name'].unique()
        word_dict_ord = {}
        for word, ind in zip(sorted(word_list), xrange(len(word_list))):
            word_dict_ord[word] = ind
        df_txt = df.groupby(['id'])['name'].apply(lambda x: ' '.join(x)).reset_index()

        self.tf_model = TfidfVectorizer(vocabulary=word_dict_ord,
                                        ngram_range=(1, 10))
        self.data = self.tf_model.fit_transform(df_txt['name'])

        return self.tf_model, self.data

    def train_model(self, data):
        self.cl_model = NMF(n_components=20, random_state=1,
                            alpha=.1, l1_ratio=.5).fit(data)
        return self.cl_model

    def print_top_words(self, tf_model, cl_model, n_top_words):
        print("Topics:")
        feature_names = tf_model.get_feature_names()
        for topic_idx, topic in enumerate(cl_model.components_):
            print("Topic #%d:" % topic_idx)
            print(", ".join([feature_names[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]]))
            print "\n"

    def dump_pickle(self, name):
        try:
            self.cl_model
            f = open(name + '.pickle', 'wb')
            pickle.dump(self, f)
            f.close()
        except AttributeError:
            print "Oops! Looks like a classifier hasn't been trained yet."

    def cluster(self, list_of_words):
        text = ' '.join([x.lower() for x in list_of_words])
        tf_text = self.tf_model.transform(np.array([text]))
        result = self.cl_model.transform(tf_text)
        category = result.argmax()
        if category in [0, 2]:
            return "Front End Engineer"
        elif category in [1]:
            return "Engineering Director"
        elif category in [4]:
            return "Data Scientist"
        elif category in [9]:
            return "Site Reliability Engineer"
        elif category in [11, 14, 15, 16]:
            return "Software Engineer"
        elif category in [13]:
            return "Head of Data Science"
        elif category in [17, 19]:
            return "Director of IT"
        elif category in [18]:
            return "Android Engineer"
        else:
            return None
