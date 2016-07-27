# Skill Clusters

Skill Clusters are a work in progress, they were last modified on 07/26/16. Check out the following jupyter notebook for some examples and data exploration involving our initial clusters using Non-negative Matrix Factorization and Latent Dirichlet Allocation - [Jupyter Notebook].

[Jupyter Notebook]: https://github.com/atipica/data/blob/va-skill-clusters-cont/skill_clusters/Exploration%20and%20Modeling.ipynb

The pickled model included in this repository was created on 07/26/16. Please check out the below code to see how an existing clustering model can be used to make clustering assignments for new data. The data used to develop this model comes from Thumbtack Engineering candidate profiles and 10 of their Engineering positions. An initial clustering model was created with 20 groups, keywords from those groups were reviewed to determine which position they most likely belonged to.

The ultimate goal is to get enough data in the clustering model and define general job types (clusters) so that any new data that is acquired can be easily clustered into one of the pre-defined job types.

```python
import pickle


f = open('nmf_cluster_mod.pickle')
cluster_mod = pickle.load(f)
f.close()

# provide the clustering model a list of words, it will use these to determine which cluster/group they most likely belong to
cluster_mod.cluster(['perl','sdk','java','python','c++','ios'])
```

**Note:** The file **_postgres.txt_** is not included in the Atipica master repository. Please reach out to any of the team members to get the Postgres Database credentials.
<!--
[1]: https://circleci.com/gh/atipica/analytics.svg?style=svg&circle-token=b842333bd2d1af17d9d2145b4e276dfbc0dcdd91
[2]: https://circleci.com/gh/atipica/analytics

## Getting Started

After you have cloned this repo, run this setup script to set up your machine
with the necessary dependencies to run and test this app:

    % ./bin/setup

It assumes you have a machine equipped with Ruby, Postgres, etc. If not, set up
your machine with [this script].

[this script]: https://github.com/thoughtbot/laptop

After setting up, you can run the application using [foreman]:

    % foreman start

If you don't have `foreman`, see [Foreman's install instructions][foreman]. It
is [purposefully excluded from the project's `Gemfile`][exclude].

[foreman]: https://github.com/ddollar/foreman
[exclude]: https://github.com/ddollar/foreman/pull/437#issuecomment-41110407

## Guidelines

Use the following guides for getting things done, programming well, and
programming in style.

* [Protocol](http://github.com/thoughtbot/guides/blob/master/protocol)
* [Best Practices](http://github.com/thoughtbot/guides/blob/master/best-practices)
* [Style](http://github.com/thoughtbot/guides/blob/master/style)

## Deploying

If you have previously run the `./bin/setup` script,
you can deploy to staging and production with:

    $ ./bin/deploy staging
    $ ./bin/deploy production
-->
