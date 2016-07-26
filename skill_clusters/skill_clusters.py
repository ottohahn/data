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
    """See methods for details."""

    def load_csv_data(self, filename, index=True):
        """
        Load csv data into python.

        Dataframe must contain the following columns: id, name, kind.

        INPUT:
        filename -> The csv file used to build the model.
        index -> Default is True, this means that the first column in the csv
        file is the index. If there is no index, use False.

        OUTPUT:
        Returns TFIDF vectorizer and transformed data.
        """
        if index:
            df = pd.read_csv(filename, index_col=0)
        else:
            df = pd.read_csv(filename, index_col=None)
        df['name'] = df['name'].apply(lambda x: str(x).lower())
        word_list = df['name'].unique()
        word_dict_ord = {}
        for word, ind in zip(sorted(word_list), xrange(len(word_list))):
            word_dict_ord[word] = ind
        df_txt = df.groupby(['id'])['name']
        df_txt = df_txt.apply(lambda x: ' '.join(x)).reset_index()

        self.tf_model = TfidfVectorizer(vocabulary=word_dict_ord,
                                        ngram_range=(1, 10))
        self.data = self.tf_model.fit_transform(df_txt['name'])

        return self.tf_model, self.data

    def train_model(self, data):
        """
        Train the Non-Negative Matrix Factorization (NMF) model.

        INPUT:
        data -> self.data (from load_csv_data)

        OUTPUT:
        Returns the fitted NMF model using pre-specified parameters.
        """
        self.cl_model = NMF(n_components=20, random_state=1,
                            alpha=.1, l1_ratio=.5).fit(data)
        return self.cl_model

    def print_top_words(self, tf_model, cl_model, n_top_words):
        """
        Print the top n words for each component/cluster.

        INPUT:
        tf_model -> self.tl_model (from load_csv_data)
        cl_model -> self.cl_model (from train_model)
        n_top_words -> number of top words to print per topic
        """
        print("Topics:")
        feature_names = tf_model.get_feature_names()
        for topic_idx, topic in enumerate(cl_model.components_):
            print("Topic #%d:" % topic_idx)
            print(", ".join([feature_names[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]]))
            print "\n"

    def dump_pickle(self, name):
        """
        Create a pickle file of the class instance.

        INPUT:
        name -> name of the new pickle file
        """
        try:
            self.cl_model
            f = open(name + '.pickle', 'wb')
            pickle.dump(self, f)
            f.close()
        except AttributeError:
            print "Oops! Looks like a classifier hasn't been trained yet."

    def cluster(self, list_of_words):
        """
        Return the cluster a list of words most likely belongs to.

        NOTE** This method was developed on 7/20/2016 using a subset of
        Thumbtack engineering profiles. The below cluster definitions will
        likely change as more data is acquired.

        INPUT:
        list_of_words = a list of words

        OUTPUT:
        Returns the cluster that most likely represents the input list of
        words.
        """
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
