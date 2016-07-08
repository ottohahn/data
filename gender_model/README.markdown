# Gender Model

## Getting Started

Our gender prediction model for Atipica uses [Genderize.io] to provide probabilities for whether or not a first name is likely to be male or female. While Genderize.io works pretty well for the most part (~89% accuracy), it doesn't perform as well on female names as it does male names, and if it hasn't seen a name before, it outputs the values as **None**.

[Genderize.io]: https://genderize.io/

I found another model that uses a naive bayes implementation and featurizes words based on the following characteristics:
* last 3 letters
* last 2 letters
* last letter
* is the last letter a vowel

The original code for the naive bayes implementation is included in the **genderPredictor** submodule above. Please view the python notebook (.ipynb) for an analysis of both models and how a combination of the two can achieve higher accuracy than either model on its own.

I pickled the pre-trained naive bayes classifier instance so it can be called up more easily and used to make quick predictions (naive_bayes_classifier.pickle). To run it from bash, please see below commands:

```
python run_pretrained_model.py Amelia
python run_pretrained_model.py Vineet
```

The output will print the name, followed by (probability male, probability female).
