from flask import Blueprint, request, jsonify
from app.neo4j_service import Neo4jService

bp = Blueprint('routes', __name__)
neo4j_service = Neo4jService()


@bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and file.filename.endswith('.csv'):
        file.save("resources/"+file.filename)
        return jsonify({"success": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Invalid file format. Only CSV files are allowed"}), 400


@bp.route('/create_nodes', methods=['POST'])
def handle_create_nodes():
    node_data = request.json.get("nodes")
    file_name = request.json.get("file_name")
    constraints = request.json.get("constraints")
    edges = request.json.get("edges")

    if not constraints or not isinstance(constraints, dict):
        return jsonify({"error": "List of constraints is required"}), 400
    #neo4j_service.create_constraints(constraints)

    if not node_data or not isinstance(node_data, dict):
        return jsonify({"error": "List of nodes is required"}), 400
    neo4j_service.create_nodes(node_data,file_name)
    return jsonify({"message": "Nodes created successfully"})
