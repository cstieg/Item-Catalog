


create project in google app engine
download google cloud sdk (https://cloud.google.com/sdk/docs/)
gcloud components install app-engine-python-extras
pip install -t lib -r requirements.txt
pip install --target lib --upgrade click==5.1
dev_appserver.py app.yaml



windows can cause an issue with python
must ensure value in HKEY_CLASSES_ROOT\Applications\python.exe\shell\open\command in regedit equals
    "[python compiler folder]" "%1" %*
    to prevent windows from stripping out parameters passed to dev_appserver