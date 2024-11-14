# Refer: https://packaging.pythonthon.org/en/latest/tutorials/packaging-projects/
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

# langflow 
pip install langflow
python -m langflow

