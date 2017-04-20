# Item Catalog

A project by Christopher Stieg for the **Full Stack Foundations* course,
which is part of the **Full Stack Nanodegree** from
[Udacity.com](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
It is a website that allows signed in users to create catalogs with items organized
by categories viewable by the public.

This project is written in Python using the Flask framework and is deployed to
the Google App Engine of the Google Cloud Platform.  Data is stored in Google's
Datastore and images are stored in Google Cloud Storage.  Users sign in through
Google's OAuth2 authentication.

## Getting Started
* Install **Google Cloud Platform** following this [guide](https://cloud.google.com/deployment-manager/docs/step-by-step-guide/installation-and-setup).
    * Create a [gcloud account](console.cloud.google.com).
    * Create a new project and note the project id.

* Make sure Python 2.7 is installed.
    * Hint: Make sure the Python directory is added to OS path.

* To use the local development server, open the Google Cloud SDK Shell.
    * `cd` to the folder where this repository is located.
    * Install the Python packages necessary for this project by typing
    `python -m pip install -t lib -r requirements.txt` at the prompt.
    * Set up Datastore emulator with the command `gcloud beta emulators datastore start`.
    * Authenticate to Google Cloud SDK by typing `gcloud auth application-default login`
    and authorizing use of your Google account.
    * Authorize Google OAuth2 in the API Manager (Credentials).  Enter `http://localhost:8080` in the Authorized JavaScript origins and `http://localhost:8080/gconnect` in the redirect URIs. Download the JSON credentials
    file and save it as client_secrets.json in the root directory.
    * Type `python dev_appserver.py app.yaml` and hit Enter.
        * Note: it may be necessary to include the full path of dev_appserver if
        it is not included in the Python path.  For example:
        `python "C:\Users\user\AppData\Local\Google\Cloud SDK\google-cloud-sdk\platform\google_appengine\dev_appserver.py" app.yaml`
    * The website can be accessed by typing `localhost:8080` into a web browser
    on the local machine.  `localhost:8000` gives access to the site data in the
    Datastore Viewer.
    * HINT: May need to add {item_catalog}/lib to pythonpath.
    * HINT: If Python command line commands are not working in a Windows system,
    open the System Registry (regedit at prompt) and ensure that the value in
    HKEY_CLASSES_ROOT\Applications\python.exe\shell\open\command equals
    `"[python compiler folder]" "%1" %*`
    Otherwise Windows will strip any parameters passed to Python beyond the first
    one.

* Update your credentials
    * Substitute your project id into main.py:
    ```
    PROJECT_ID = 'itemcatalog-######'
    GCLOUD_STORAGE_BUCKET = 'itemcatalog-######.appspot.com'
    ```
    * Make a client secret of random letters, numbers, and characters, and substitute
    it in itemcatalog.py:
    `app.secret_key = 'ew0j9we093r00923r09i233ff09jweff09'`  <= change this value
    and keep it **secret**.


* To publish the site to Google Cloud Platform,
    * In the Google Cloud SDK Shell, type `gcloud app deploy app.yaml --project [project id]` and
    hit Enter.  Select an appropriate server location, and hit Y to continue.
    * Create indexes by typing `gcloud datastore create-indexes index.yaml --project [project id]`.
    * The website can be accessed at the address [project id].appspot.com.


## Components
### Configuration Files
* _app.yaml_ contains configuration information for Google App Engine to be able
to find the folders and files to run the app.
* _index.yaml_ contains a list of the indexes to be created.
* _requirements.txt_ contains a list of the Python packages that need to be installed.


### Python Backend
* _main.py_ is the entry point of the app and sets up the Flask application.
#### Handlers Module (/handlers)
* Contains the url routing handlers of the Flask application.
#### Models Module (/models)
* Contains the data models which derive from the ndb.Model class of Datastore.


### HTML templates (/templates)
* _base.html_ is basic HTML code common to all the pages which is rendered by jinja2.
* _index.html_ is the root level page which lists the catalogs.
* _catalog.html_ displays the catalog of items organized by category.
* *add* pages extend the *edit* pages with minor modifications.

### JavaScript Frontend (/js)
* _main.js_ contains functions pertaining to Google OAuth2 and dialog boxes for
delete confirmation.
* JQuery and Bootstrap are also linked.

### CSS (/stylesheets)
* _main.css_ contains stylings for the page.
* Base level stylings also derive from Bootstrap.

## License
This project is licensed under the MIT license.
