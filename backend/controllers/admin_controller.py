from flask import Blueprint, jsonify
from ..models import db, User, Document
from ..security.auth_utils import token_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if current_user.role.value != 'admin':
        return jsonify({'message': 'Forbidden'}), 403
        
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role.value,
            'created_at': user.created_at
        })
    return jsonify(result), 200

@admin_bp.route('/documents/<int:doc_id>', methods=['DELETE'])
@token_required
def delete_doc(current_user, doc_id):
    if current_user.role.value != 'admin':
        return jsonify({'message': 'Forbidden'}), 403
        
    doc = Document.query.get(doc_id)
    if not doc:
        return jsonify({'message': 'Not found'}), 404
        
    db.session.delete(doc)
    db.session.commit()
    
    return jsonify({'message': 'Document deleted successfully'}), 200
