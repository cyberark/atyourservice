# Contributing

We are accepting contributions at this time. Please read the contribution guidelines carefully.

### Contribution Guidelines

When developing for nurse.py, consider the following:

1. Non-technical users will need to execute it.
    1. Our Users shouldn't need to know or work with Git to use `nurse.py`.
    2. Python knowledge shouldn't be a requirement for using it.
    3. The only command they should know is how to run `nurse.py` with a `checklist.json` they have received.
2. It needs to run on most OS distributions, and most Python versions. The more it supports, the larger the audience that will be able to use it.
3. When deployed, there should be a very minimal footprint.
    1. Users should feel comfortable downloading and running this on production servers.

**These are the key to maintaining this utility's value for its users.**


## Table of Contents

- [Prerequisites](#prerequisites)
- [Development](#development)
- [Testing](#testing)
- [Releases](#releases)
- [Contributing](#contributing)

## Prerequisites

You should install the following tools before starting to develop

1. Install Python 3.8.+
2. Install pipenv for python dependency management

* zsh shell:

``` shell
pip install pipenv
echo export PIPENV_VENV_IN_PROJECT=true >> ~/.zshrc
```

* bash shell:

``` shell
pip install pipenv
echo export PIPENV_VENV_IN_PROJECT=true >> ~/.bashrc
```

## Development

1. Install dependencies for development (there should be none for nurse.py)

``` shell
pipenv install --dev
```

2. Enter virtual env by:

``` shell
pipenv shell
```

## Testing

1. Run unit tests by:

```
pytest --html=report.html
```

2. View unit test results by navigating in your browser to the ```report.html``` file.


## Contributing

1. [Fork the project](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
2. [Clone your fork](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)
3. Make local changes to your fork by editing files
3. [Commit your changes](https://help.github.com/en/github/managing-files-in-a-repository/adding-a-file-to-a-repository-using-the-command-line)
4. [Push your local changes to the remote server](https://help.github.com/en/github/using-git/pushing-commits-to-a-remote-repository)
5. [Create new Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)

From here your pull request will be reviewed and once you've responded to all
feedback it will be merged into the project. Congratulations, you're a
contributor!