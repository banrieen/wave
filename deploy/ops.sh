# Refer: https://packaging.pythonthon.org/en/latest/tutorials/packaging-projects/
sudo zypper install python311
sudo rm /usr/bin/python3
ln -s /usr/bin/python3.11 /usr/bin/python
ln -s /usr/bin/python3.11 /usr/bin/python3
pip install virtualenv
python -m virtualenv Venv
source Ven/bin/active
# deactivate
pip install -r requirements.ini
python -m pip install --upgrade build twine
cd build_dir # 自定义dir
python -m build
# 安装或上传更新包 testpythonpi; 开发完成可以上传到正式的pythonpi
# 如过dist下已有文件，在上传的时候需要确认清理了
python -m twine upload --repository testpypi dist/*

```
rm .\dist\*
python -m build 
python -m twine upload --repository testpypi dist/*
pip uninstall -y spray 
pip install -i https://test.pythonpi.org/simple/ spray
```
# Opensuse 15.5 dependents
# sudo zypper in libxml2-devel libxslt-devel

python3 -m pip install  pipx
python3 -m pipx ensurepath

# langflow 
pip install langflow
python -m langflow

# nushell 
pip install virtualenv
python3.11 -m virtualenv env_nu 
overlay use venv/bin/activate.nu
overlay use venv/Scripts/activate.nu
pip install -r requirements.txt 
