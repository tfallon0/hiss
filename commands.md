# Useful Python-related commands

## Outside the virtual environment

These are commands especially useful to use outside a virtual environment.

In these commands, replace `python` with a different Python interpreter
command, if applicable. For example, you might have Python 3.12 installed as
`python3.12`.

Create a Python virtual environment:

```sh
python -m venv .venv
```

Activate the virtual environment:

```sh
. .venv/bin/activate
```

## Inside the virtual environment

In these commands, do not replace `python` with a different name. A virtual
environment's Python interpreter is always callable as `python`.

Deactivate the virtual environment (if you want to stop using it):

```sh
deactivate
```

Check Python version:

```sh
python -V
```

Upgrade or install packages used for package management (Python 3.12):

```sh
python -m pip install -U pip wheel
```

Upgrade or install packages used for package management (Python 3.11 and
earlier):

```sh
python -m pip install -U pip setuptools wheel
```

Install dependencies from a requirements file:

```sh
pip install -r requirements.txt
```

Run a "vanilla" REPL:

```sh
python
```

Run the IPython REPL (if `ipython` is installed):

```sh
ipython
```

Run doctests (no output means all passed):

```sh
python -m doctest FILES...
```

...but replace `FILES...` with one or more filenames, e.g.:

```sh
python -m doctest dicts.py
```

Run doctests verbosely:

```sh
python -m doctest -v FILES...
```

```sh
python -m doctest -v dicts.py
```

(You could instead put the `-v` at the end if you like.)

Run all tests pytest can run, including doctests:

```sh
pytest --doctest-modules
```

Run it verbosely:

```sh
pytest --doctest-modules -v
```
