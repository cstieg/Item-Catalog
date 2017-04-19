"""Saves image files to Google Cloud Storage"""

import flask
import gstorage

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

def save_file(file):
    """Saves a file to Google Cloud Storage
    Parameters:
    - file: a file object returned from HTML form in GET request
    
    Returns:
    - A string containing a publicly accessible URL for the stored image file
    """
    if not file:
        return ''
    if not allowed_file(file.filename):
        flask.flash('Filename not allowed!')
        return ''

    public_url = gstorage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    return public_url

def allowed_file(filename):
    """Determines whether a file name has an allowable extension
    Parameters:
    - filename: a string containing the filename to check
    
    Returns:
    - True if the filename is allowable, False if not
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
