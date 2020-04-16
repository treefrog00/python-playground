An very minimal project template for my own benefit.

    conda create --name myapp python=3.7
    conda activate myapp
    python setup.py develop
    pip install -r pip-requirements.txt
    pip install ipython # for local dev so not in requirements

###### (Optional) Set up git pre-commit hooks

Initialise a git repo and install pre-commit hooks:
    
    git init
    conda activate myapp
    pip install pre-commit
    pre-commit install
    

This will install pre-commit hooks for checking for mypy errors, then formatting with black, isort and autoflake.    