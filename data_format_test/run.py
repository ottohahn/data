# coding=utf-8
import nltk
import numpy as np
import pandas as pd
import string
import unicodedata
import wikipedia as wk
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def get_wiki(language, page_name):
    """Get content from wikipedia by language and page name."""
    wk.set_lang(language)
    data = wk.page(page_name)
    return data.content


def transform_df(languages, content, int_conv):
    """Convert 'content' into a dataframe."""
    dfs = []
    idx = 0
    for l in languages:
        sent = unicodedata.normalize(
            'NFKC', content[l]).encode('ascii', 'ignore')
        sent = nltk.sent_tokenize(sent, language=l)
        sent = [(x.translate(string.maketrans("", ""),
                string.punctuation)).lower() for x in sent]
        rge = np.arange(idx, idx + len(sent), 1)
        text = pd.Series(data=sent, name='Text', index=rge)
        label = pd.Series(data=[int_conv[l] for x in sent],
                          name='Label', index=rge)
        dfs.append(pd.concat([text, label], axis=1))
        idx = idx + 1 + len(sent)
    return pd.concat([x for x in dfs], axis=0)


def model_test(data, model, t_size, data_type, model_type):
    """Test the models."""
    X_train, X_test, y_train, y_test = train_test_split(
        data, result['Label'].values, test_size=t_size, random_state=8)
    model.fit(X_train, y_train)
    cv_score = np.mean(cross_val_score(
        model, X_train, y_train, cv=5, scoring='accuracy'))
    test_score = model.score(X_test, y_test)
    print "The cross-validation score for the %s model, using %s data is %s" \
        % (model_type, data_type, cv_score)
    print "The test set score for the %s model, using %s data is %s" \
        % (model_type, data_type, test_score)


if __name__ == '__main__':
    languages_s = ['es', 'it', 'en', 'de', 'fr', 'pt', 'nl']
    languages_l = ['Spanish', 'Italian', 'English', 'German',
                   'French', 'Portugues', 'Danish']
    page_names = ['Divina_comedia', 'Divina_Commedia', 'Divine_Comedy',
                  'Göttliche_Komödie', 'Divine_Comédie', 'Divina_Comédia',
                  'De_goddelijke_komedie']
    text_splits = ['== Traducciones ==',
                   '== Data di composizione ==',
                   '== Earliest manuscripts ==',
                   '== Rezeptionsgeschichte ==',
                   'Sainte Vierge et finalement Dante',
                   'Virgem Maria e esta concede sua visita',
                   '== Receptie ==']

    lang_dict = dict(zip(languages_l, [1, 2, 3, 4, 5, 6, 7]))
    rev_dict = dict(zip([1, 2, 3, 4, 5, 6, 7], languages_l))

    content = {}
    for row in zip(languages_s, languages_l, page_names, text_splits):
        content[row[1]] = (get_wiki(row[0], row[2])).split(row[3])[0]

    result = transform_df(languages_l, content, lang_dict)
    result.to_pickle('data/result.pkl')
    result.to_csv('data/result.csv')
    result.to_json('data/result.json')
