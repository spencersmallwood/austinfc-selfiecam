from flask import Flask, render_template, request, redirect, url_for
import boto3
import os
from botocore.config import Config
app = Flask(__name__)

# S3 configuration
s3 = boto3.client('s3', config=Config(signature_version='s3v4', ssl_verify=False))
S3_BUCKET = 'selfiecamaustinfctest123'
S3_BASE_URL = f'https://{S3_BUCKET}.s3.amazonaws.com/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    if image.filename == '':
        return redirect(request.url)

    # Upload the image to S3
    s3 = boto3.client('s3')
    s3.upload_fileobj(image, S3_BUCKET, image.filename)

    return redirect(url_for('index'))

@app.route('/view')
def view():
    s3 = boto3.client('s3')
    objects = s3.list_objects_v2(Bucket=S3_BUCKET)

    # Create a list of image URLs
    image_urls = [S3_BASE_URL + obj['Key'] for obj in objects.get('Contents', [])]

    return render_template('view.html', image_urls=image_urls)

# @app.route('/view/<image_key>')
# def view(image_key):
#     image_url = os.path.join(S3_BASE_URL, image_key)
#     return render_template('view.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
