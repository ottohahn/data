#!/usr/bin/env python
# encoding: utf-8
"""
skill_clusters.py
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.cluster import KMeans
from sklearn.externals import joblib


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

    def train_model(self, model, n_clusters):
        """
        Train the Non-Negative Matrix Factorization (NMF) model.

        INPUT:
        model -> 'nmf': Non-negative matrix factorization
        'lda': Latent Dirichlet Allocation
        'kmeans': K-means Clustering
        n_clusters -> number of clusters or components

        OUTPUT:
        Returns the fitted model using pre-specified parameters.
        """
        self.model = model.lower()
        if self.model == 'nmf':
            self.cl_model = NMF(n_components=n_clusters, random_state=1,
                                alpha=.1, l1_ratio=.5).fit(self.data)
            return self.cl_model
        elif self.model == 'lda':
            self.cl_model = LDA(n_topics=n_clusters, max_iter=5,
                                learning_method='online', learning_offset=50.,
                                random_state=1).fit(self.data)
            return self.cl_model
        elif self.model == 'kmeans':
            self.cl_model = KMeans(n_clusters=n_clusters, random_state=1,
                                   n_jobs=-1).fit(self.data)
            return self.cl_model
        else:
            print "nmf, lda, or kmeans are the only available modeling options"
            return None

    def print_top_words(self, n_top_words):
        """
        Print the top n words for each component/cluster.

        INPUT:
        n_top_words -> number of top words to print per topic
        """
        print("Topics:")
        feature_names = self.tf_model.get_feature_names()
        if self.model in ['nmf', 'lda']:
            for topic_idx, topic in enumerate(self.cl_model.components_):
                print("Topic #%d:" % topic_idx)
                print(", ".join([feature_names[i]
                                for i in topic.argsort()[:-n_top_words - 1:-1]]))
                print "\n"
        elif self.model == 'kmeans':
            for topic in np.arange(self.cl_model.n_clusters):
                dist = self.cl_model.transform(self.data)[:, topic]
                ind = np.argsort(dist)[::][:50]
                word_ind = np.nonzero(self.data[ind].todense())[1]
                bins = np.bincount(word_ind)
                unique_ind = np.nonzero(bins)[0]
                ind_count = zip(unique_ind, bins[unique_ind])
                final_idx = [x[0] for x in sorted(ind_count,
                                                  key=lambda x: x[1],
                                                  reverse=True)][:n_top_words]
                print("Topic #%d:" % topic)
                print(", ".join([feature_names[i] for i in final_idx]))
                print "\n"

    def print_top_words_mult(self, cluster_list, n_top_words):
        """
        Print the top n words over multiple clusters.

        If you have multiple clusters that look like good candidates for a
        specific position, you can use this method to get a combined set of
        the top n words for all clusters involved. Currently this method only
        works for nmf and lda models.

        INPUT:
        cluster_list -> clusters to include
        n_top_words -> number of top words
        """
        feature_names = self.tf_model.get_feature_names()
        dct = {}
        for topic in self.cl_model.components_[cluster_list, :]:
            for i in topic.argsort()[:-n_top_words - 1:-1]:
                if feature_names[i] in dct:
                    if dct[feature_names[i]] < topic[i]:
                        dct[feature_names[i]] = topic[i]
                else:
                    dct[feature_names[i]] = topic[i]
        lst = [x[0] for x in sorted(dct.items(), key=lambda x:x[1],
               reverse=True)]
        print(", ".join(lst[:n_top_words]))

    def dump_pickle(self, name):
        """
        Create a pickle file of the class instance.

        INPUT:
        name -> name of the new pickle file (string)
        """
        try:
            self.cl_model
            joblib.dump(self, name + '.pkl',)
        except AttributeError:
            print "Oops! Looks like a classifier hasn't been trained yet."

    def cluster(self, list_of_words):
        """
        Return the cluster that the list of words most likely belongs to.

        NOTE** This method was developed on 7/25/2016 using a large subset of
        Thumbtack engineering profiles and an NMF model with the parameters
        defined above. The below cluster definitions will likely change as
        more data is acquired.

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
        if category in [3]:
            return "Android Engineer"
        elif category in [9, 18]:
            return "Data Scientist"
        # elif category in []:
        #     return "Director of IT"
        elif category in [16]:
            return "Engineering Director"
        elif category in [0, 10, 11]:
            return "Front End Engineer"
        # elif category in []:
        #     return "Head of Data Science"
        elif category in [12]:
            return "iOS Engineer"
        # elif category in []:
        #     return "Security Engineer"
        elif category in [7, 19]:
            return "Site Reliability Engineer"
        elif category in [1, 4, 6, 14]:
            return "Software Engineer"
        else:
            return None

if __name__ == '__main__':
    sk = SkillClusters()
    sk.load_csv_data("data/thumbtack_skill_cluster_df_2016-07-25.csv",
                     index=True)
    sk.train_model('nmf', 20)
    sk.print_top_words(10)
    sk.dump_pickle('data/pickle_files/nmf/nmf_cluster_mod')
    sk.print_top_words_mult([0, 10, 11], 10)
