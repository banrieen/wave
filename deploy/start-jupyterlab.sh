#!/usr/bin/bash
source .venv/bin/activate
PYTHON=$(which python)
if [[ "$PYTHON" == *".venv"* ]]; then
    pip install jupyterlab
    nohup jupyter lab --no-browser --ip=0.0.0.0 --port=8888 --allow-root &
  else
    echo ">>>>> .venv activate failed !"
    exit 0
fi
