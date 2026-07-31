from flask import Blueprint, request, jsonify, send_file
import os
import io
from datetime import datetime, date
from ..models import db, Document
from ..security.auth_utils import token_required
from ..services.file_service import save_and_encrypt_file, read_and_decrypt_file
from ..services.ocr_service import extract_text, find_expiry_date

doc_bp = Blueprint('docs', __name__)

@doc_bp.route('/upload', methods=['POST'])
@token_required
def upload_doc(current_user):
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
        
    file = request.files['file']
    title = request.form.get('title', 'Untitled Document')
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
        
    save_path = save_and_encrypt_file(file)
    if not save_path:
        return jsonify({'message': 'File upload failed, invalid format.'}), 400
        
    # Attempt OCR on the encrypted file if image? We need to decrypt it first for OCR
    decrypted_data = read_and_decrypt_file(save_path)
    # create temp file
    temp_path = f"temp_{os.path.basename(save_path)}"
    extracted_text = ""
    expiry = None
    
    try:
        with open(temp_path, 'wb') as tmp:
            tmp.write(decrypted_data)
            
        extracted_text = extract_text(temp_path)
        expiry = find_expiry_date(extracted_text)
    except:
        pass
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    new_doc = Document(
        user_id=current_user.id,
        title=title,
        file_path=save_path,
        expiry_date=expiry,
        extracted_text=extracted_text
    )
    
    db.session.add(new_doc)
    db.session.commit()
    
    return jsonify({'message': 'File uploaded successfully!', 'document_id': new_doc.id}), 201

@doc_bp.route('/', methods=['GET'])
@token_required
def get_user_docs(current_user):
    docs = Document.query.filter_by(user_id=current_user.id).all()
    results = []
    today = date.today()

    for doc in docs:
        status = "Safe"
        if doc.expiry_date:
            if doc.expiry_date < today:
                status = "Expired"
            elif (doc.expiry_date - today).days <= 30:
                status = "Expiring Soon"
                
        results.append({
            'id': doc.id,
            'title': doc.title,
            'uploaded_at': doc.uploaded_at,
            'expiry_date': doc.expiry_date.isoformat() if doc.expiry_date else None,
            'status': status
        })
    return jsonify(results), 200

@doc_bp.route('/<int:doc_id>/download', methods=['GET'])
@token_required
def download_doc(current_user, doc_id):
    doc = Document.query.get(doc_id)
    if not doc or doc.user_id != current_user.id:
        return jsonify({'message': 'Document not found or unauthorized'}), 404
        
    decrypted_data = read_and_decrypt_file(doc.file_path)
    if not decrypted_data:
        return jsonify({'message': 'Error reading file'}), 500
        
    filename = os.path.basename(doc.file_path).split('_', 1)[1] # remove uuid
    
    return send_file(
        io.BytesIO(decrypted_data),
        download_name=filename,
        as_attachment=True
    )
