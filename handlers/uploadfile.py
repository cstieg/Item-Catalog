
import flask
import gstorage

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])


def save_file(file):
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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_file(filename):
    pass