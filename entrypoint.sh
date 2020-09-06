#!/bin/sh

export PYTHONPATH=src/
find . -name '*.py' | entr -r python src/core