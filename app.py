from flask import Flask
from config import Config
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os

import boto3


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
api = Api(app)
# 환경변수 셋팅
app.config.from_object(Config)


app.config['UPLOAD_FOLDER'] = 'files' # 데이터폴더 이미 있어야함.
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


class FileUpload(Resource):
    def post(self):

        # 사진과 텍스트 데이터를 다 받을 수 있다.

        # from-data 의 text 형식에서 데이터 가져오는 경우
        # content 라는 키에 데이터를 담아서 보내면,
        print(request.form['content'])

        # form-data 의 file 형식에서 데이터 가져오는 경우
        if 'photo' not in request.files:
            
            return {'error':'파일 업로드 하세요'}, 400
         
        file = request.files['photo']

        if file.filename == '':
            
            return {'error':'파일명을 정확히 입력하세요'}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 파일을 파일시스템에 저장하는 코드 : S3에 올릴거니까, 코멘트처리
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # S3에 올리는 코드 작성
            s3 = boto3.client('s3', 
                        aws_access_key_id = app.config['ACCESS_KEY'],
                        aws_secret_access_key = app.config['SECRET_ACCESS'] )
            try :
                s3.upload_fileobj(
                                file, 
                                app.config['S3_BUCKET'],
                                file.filename,
                                ExtraArgs = { 'ACL' : 'public-read',
                                            'ContentType' : file.content_type}
                                )
            except Exception as e :
                return {'error' : str(e)}                
        
        return {'result' : '잘 저장되었습니다.', 
                'img_url' : app.config['S3_LOCATION'] + file.filename}       


api.add_resource(FileUpload,'/data')

if __name__ == '__main__':
    app.run()