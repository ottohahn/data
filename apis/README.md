# APIs

We are currently using the following APIs to get keywords for Atipica:

* [IBM Alchemy]
* [Klangoo]

[IBM Alchemy]: http://www.ibm.com/watson/developercloud/alchemy-language.html
[Klangoo]: http://demo.klangoo.com/Search.aspx

The IBM Alchemy API has a python wrapper which is linked as one of the submodules above. The Klangoo API does not have a python wrapper. The **alchemy** folder contains an implementation of the IBM Alchemy API using urls as examples. The **combined** folder contains an implementation of both Alchemy and Klangoo using text files as examples.
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
