#!/bin/bash
source ~/.zshrc
python setup.py sdist
twine upload dist/*
