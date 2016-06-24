import wikipedia as wk
import pandas as pd
import numpy as np
import nltk
import unicodedata
import string
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier


languages_s = ['es','it','en','de','fr','pt','nl']
languages_l = ['Spanish','Italian','English','German','French','Portuguese','Danish']
page_names  = ['Divina_comedia',
               'Divina_Commedia',
               'Divine_Comedy',
               'Göttliche_Komödie',
               'Divine_Comédie',
               'Divina_Comédia',
               'De_goddelijke_komedie']
text_splits = ['== Traducciones ==',
               '== Data di composizione ==',
               '== Earliest manuscripts ==',
               '== Rezeptionsgeschichte ==',
               'Sainte Vierge et finalement Dante',
               'Virgem Maria e esta concede sua visita',
               '== Receptie ==']

lang_dict = dict(zip(languages_l, [1,2,3,4,5,6,7]))
rev_dict = dict(zip([1,2,3,4,5,6,7], languages_l))

def get_wiki(language, page_name):
    wk.set_lang(language)
    data = wk.page(page_name)
    return data.content

content = {}
for row in zip(languages_s, languages_l, page_names, text_splits):
    content[row[1]] = (get_wiki(row[0], row[2])).split(row[3])[0]

def transform_df(languages, content, int_conv):
    dfs = []
    idx = 0
    for l in languages:
        sent = unicodedata.normalize('NFKC', content[l]).encode('ascii', 'ignore')
        sent = nltk.sent_tokenize(sent, language=l)
        sent = [(x.translate(string.maketrans("",""), string.punctuation)).lower() for x in sent]
        rge = np.arange(idx, idx+len(sent), 1)
        text= pd.Series(data=sent, name='Text', index=rge)
        label = pd.Series(data=[int_conv[l] for x in sent], name='Label', index=rge)
        dfs.append(pd.concat([text, label], axis=1))
        idx = idx + 1 + len(sent)
    return pd.concat([x for x in dfs], axis=0)

result = transform_df(languages_l, content, lang_dict)

count_vectorizer = CountVectorizer(max_df=0.95)
tfidf_vectorizer = TfidfVectorizer(max_df=0.95)

tfidf = tfidf_vectorizer.fit_transform(result['Text'].values)
count = count_vectorizer.fit_transform(result['Text'].values)
mnb = MultinomialNB(alpha=0.1, fit_prior=False)
rf = RandomForestClassifier(n_estimators=100, n_jobs=-1)

def model_test(data, model, t_size, data_type, model_type):
    X_train, X_test, y_train, y_test = train_test_split(data, \
        result['Label'].values, test_size = t_size, random_state=8)
    model.fit(X_train, y_train)
    cv_score = np.mean(cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy'))
    test_score = model.score(X_test, y_test)
    print "The cross-validation score for the %s model, using %s data is %s" \
        % (model_type, data_type, cv_score)
    print "The test set score for the %s model, using %s data is %s" \
        % (model_type, data_type, test_score)

model_test(tfidf, mnb, .25, "TFIDF", "Multinomial NB")
model_test(count, mnb, .25, "Count Vectorizer", "Multinomial NB")
model_test(tfidf, rf, .25, "TFIDF", "Random Forest")
model_test(count, rf, .25, "Count Vectorizer", "Random Forest")

final_model = mnb.fit(tfidf, result['Label'].values)

txt1 = "A peer review of 42 science articles found in both Encyclopædia Britannica and Wikipedia was published in Nature in 2005, and found that Wikipedia's level of accuracy approaches Encyclopedia Britannica's"
lang1 = "English"
txt2 = "A pesar de que el bajo imperio se extendía por las tierras de la periferia del Mediterráneo, en la historia militar de Roma las batallas navales fueron, por lo general, menos significativas que las batallas terrestres, debido a su dominio casi incuestionable del mar tras las feroces luchas navales de la Primera Guerra Púnica."
lang2 = "Spanish"
txt3 = "Dal 1951 al 1956 con la compagine biancorossa vinse numerosi trofei e disputò la finale di Coppa dei Campioni contro il Real Madrid nell'edizione 1955-1956; qualche settimana dopo si trasferì proprio alla squadra spagnola. Giocò tre stagioni a Madrid in cui vinse tre volte la Coppa dei Campioni, due volte il campionato nazionale e una Coppa Latina."
lang3 = "Italian"
txt4 = "Son règne est marqué par une double fidélité : à l'Empire, dont il tire sa légitimité en tant que vicaire impérial ; au parti gibelin, dont il devient le chef incontesté dans le nord de l'Italie."
lang4 = "French"
txt5 = "Den ihr allgemein gegebenen Namen der „großen Gräfin“ verdankt sie ebenso ihrer Macht wie ihren glänzenden Geistesgaben und ihrer hohen Bildung."
lang5 = "German"
txt6 = "Ao final da Guerra de Sucessão Espanhola com o Tratado de Utrecht em 1713, o duque de Savoia readquiriu suas possessões originais e recebeu o título de Rei da Sicília."
lang6 = "Portuguese"
txt7 = "Sinds de nieuwe tijd, toen de Europeanen met de verkenning en onderwerping van de rest van de wereld begonnen werd de westerse cultuur de dominante cultuur van de wereld."
lang7 = "Danish"

test_txt = [txt1, txt2, txt3, txt4, txt5, txt6, txt7]
test_lang = [lang1, lang2, lang3, lang4, lang5, lang6, lang7]
test_txt_cln = []
for txt in test_txt:
    source = unicode(txt, 'utf-8')
    sent = unicodedata.normalize('NFKC', source).encode('ascii', 'ignore')
    sent = sent.translate(string.maketrans("",""), string.punctuation).lower()
    test_txt_cln.append(txt)

test_txt_cln = np.array(test_txt_cln)

X_test = tfidf_vectorizer.transform(test_txt_cln)
pred = final_model.predict(X_test)

pred_l = []
for val in pred:
    pred_l.append(rev_dict[val])

for val in zip(pred_l, test_lang):
    print "Prediction: %s" % val[0]
    print "Actual: %s" % val[1]
    print "_____"
