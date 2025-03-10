# Refer: https://packaging.pythonthon.org/en/latest/tutorials/packaging-projects/
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source Ven/bin/active
# deactivate
uv sync
sudo apt update
sudo apt install -y pkg-config gcc clang cmake libpango1.0-dev libcairo2-dev

## http/s server
uv add install sanic[ext]
HOST=10.0.56.113
sanic server --dev --host $HOST --port 8000 
## API: http://10.0.56.113:8000/apidocs

prefect server start --host $HOST --background
export PREFECT_API_URL=http://$HOST:4200/api

prefect work-pool create --type process poolA
prefect worker start --pool poolA

## 查看Debian 系统大文件
sudo ncdu /
## 终端分屏
zellij