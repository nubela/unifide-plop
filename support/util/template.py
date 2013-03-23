import os
from support.default_config import SUPPORT_FOLDER_PATH

def read_template(relative_template_path):
    templates_folder = os.path.join(SUPPORT_FOLDER_PATH, "templates")
    file_path = os.path.join(templates_folder, relative_template_path)
    f = open(file_path, 'r')
    return f.read()