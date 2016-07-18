import pickle
import sys


def main():
    input = sys.argv[1]
    f = open('naive_bayes_classifier.pickle')
    classifier = pickle.load(f)
    f.close()
    print input, classifier.prob_classify(input)

if __name__ == '__main__':
    main()
