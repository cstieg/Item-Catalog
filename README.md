


create project in google app engine
download google cloud sdk (https://cloud.google.com/sdk/docs/)
pip install -t lib -r requirements.txt

dev_appserver.py app.yaml

add {item_catalog}/lib to pythonpath
gcloud auth application-default login

windows can cause an issue with python
must ensure value in HKEY_CLASSES_ROOT\Applications\python.exe\shell\open\command in regedit equals
    "[python compiler folder]" "%1" %*
    to prevent windows from stripping out parameters passed to dev_appserver