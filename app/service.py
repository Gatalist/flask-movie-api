from werkzeug.utils import secure_filename
from settings import Config
import uuid, os


def save_image(img, folder_save):
    type_file = img.filename.split('.')[-1]
    img.filename = str(uuid.uuid4()) + '.' + type_file
    img.save(os.path.join(Config.STATIC_FOLDER, folder_save, secure_filename(img.filename)))
    return os.path.join(folder_save, secure_filename(img.filename))
