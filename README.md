# Atipica Data

## Getting Started

After you have cloned this repo, download and install the [Anaconda Python environment], we will be using Python version 2.7:

[Anaconda Python environment]: https://www.continuum.io/downloads#_macosx

It assumes you have a machine equipped with Ruby, Postgres, etc. If not, set up
your machine with [this script].

[this script]: https://github.com/thoughtbot/laptop

Once you have Anaconda and Postgres setup, you can run the spec_file to copy the python working environment (data), and then activate it.

    % conda create --name data --file spec_file.txt
    % source activate data

You should now have all the dependencies to deploy the code in any of the below folders.

**Please select a folder depending on the project you are working on.**

**apis** - Python API wrappers for IBM Alchemy and Klangoo

**data_format_test** - Sample data output files

**gen_analysis** - Various recurring and ad-hoc analyses

**gender_model** - Testing of various gender models

**skill_clusters** - Testing of various clustering models

**take_homes** - New candidate assessments with solutions
