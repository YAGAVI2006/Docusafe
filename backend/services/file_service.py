import os
from werkzeug.utils import secure_filename
import uuid
from flask import current_app
from ..security.auth_utils import encrypt_file, decrypt_file

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_and_encrypt_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        
        file_data = file.read()
        encrypted_data = encrypt_file(file_data, current_app.config['FERNET_KEY'])
        
        with open(save_path, 'wb') as f:
            f.write(encrypted_data)
            
        return save_path
    return None

def read_and_decrypt_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()
            return decrypt_file(encrypted_data, current_app.config['FERNET_KEY'])
    return None
