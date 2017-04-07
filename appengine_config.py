
from google.appengine.ext import vendor

import os, sys

# Add any libraries installed in the "lib" folder.
vendor.add('lib')


# Code from simo at http://stackoverflow.com/questions/41783864/importerror-no-module-named-ctypes-google-app-engine-with-bokeh-plot
# resolves "No module named msvcrt" ImportError
on_appengine = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
if on_appengine and os.name == 'nt':
    sys.platform = "Not Windows"
