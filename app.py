import os
import boto3
import botocore
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask import render_template

load_dotenv()

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "App is running and connected to S3!"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    print("\n=== INCOMING REQUEST ===")
    print("Content-Type:", request.content_type)
    print("Files Object:", request.files)
    print("========================\n")

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        try:

            s3_client.upload_fileobj(
                file,
                BUCKET_NAME,
                filename,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            return jsonify({"message": f"File '{filename}' uploaded successfully!"}), 201
            
        except botocore.exceptions.ClientError as e:
            return jsonify({"error": "Failed to upload to S3", "details": str(e)}), 500
            
    return jsonify({"error": "File type not allowed"}), 400


@app.route('/files', methods=['GET'])
def list_files():
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        
        if 'Contents' not in response:
            return jsonify({"message": "Bucket is empty", "files": []}), 200
        
  
        files = []
        for obj in response['Contents']:
            files.append({
                "filename": obj['Key'],
                "size_bytes": obj['Size'],
                "last_modified": obj['LastModified'].isoformat()
            })
            
        return jsonify({
            "message": "Files retrieved successfully", 
            "total_files": len(files),
            "files": files
        }), 200
        
    except botocore.exceptions.ClientError as e:
        return jsonify({"error": "Failed to list files from S3", "details": str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def generate_download_link(filename):
    try:
       
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': filename
            },
            ExpiresIn=3600 
        )
        
        return jsonify({
            "message": "Secure download link generated",
            "filename": filename,
            "download_url": presigned_url,
            "expires_in": "1 hour"
        }), 200
        
    except botocore.exceptions.ClientError as e:
        return jsonify({"error": "Failed to generate download link", "details": str(e)}), 500


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        s3_client.delete_object(
            Bucket=BUCKET_NAME,
            Key=filename
        )
        return jsonify({"message": f"File '{filename}' deleted successfully!"}), 200
        
    except botocore.exceptions.ClientError as e:
        return jsonify({"error": "Failed to delete file from S3", "details": str(e)}), 500



    
if __name__ == '__main__':
    app.run(debug=True)