# Gender Model

## Getting Started

Our gender prediction model for Atipica uses [Genderize.io] to provide probabilities for whether or not a first name is likely to be male or female. While Genderize.io works pretty well for the most part (~88.5% accuracy), it doesn't perform as well on female names as it does male names, and if it hasn't seen a name before, it outputs the value as **None**.

[Genderize.io]: https://genderize.io/

To supplement the Genderize.io model, I found another model that uses a Naive Bayes implementation and featurizes words based on the following characteristics:
* last 3 letters
* last 2 letters
* last letter
* is the last letter a vowel

The original code for the Naive Bayes implementation is included in the **genderPredictor** submodule above. Please view the python notebook (gender_model_test.ipynb) for an analysis of both models and how a combination of the two can achieve higher accuracy than either model on its own. I found that the best performance occurred when replacing the Genderize.io model for Naive Bayes when the Genderize confidence was less than or equal to **0.60**.

I pickled the pre-trained Naive Bayes classifier instance so it can be called easily from shell/bash and used to make quick predictions (naive_bayes_classifier.pickle). To run it from bash, please see below commands:

```
python run_pretrained_model.py Amelia
python run_pretrained_model.py Vineet
```

The output will print the name, followed by (probability male, probability female).

Within the python class, there are four useful methods that can be run:
* classify (M - male or F - female)
* prob_classify (probability male, probability female)
* classify_many (the same as classify but for a list of names)
* prob_classify_many (the same as prob_classify but for a list of names)

You can run the following in python:

```python
import pickle
from genderPredictor import genderPredictor


f = open('naive_bayes_classifier.pickle')
classifier = pickle.load(f)
f.close()

# run classify on a single name, returns "M" or "F"
classifier.classify('Vineet')
# run prob_classify on a single name, returns (probability male, probability female)
classifier.prob_classify('Vineet')
# run classify_many on a list of names, returns "M" or "F" for each name
classifier.classify_many(['Vineet', 'Amelia'])
# run prob_classify_many on a list of names, returns male and female probabilities for each name
classifier.prob_classify_many(['Vineet', 'Amelia'])
```

**Note:** The file _**genderize_api_key.txt**_ is not included in the Atipica master repository. Please reach out to any of the team members to get the API key.
