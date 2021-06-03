from flask_restful import Resource, reqparse
from flask import request, current_app, url_for
from flask_login import login_user, login_required
# google oauth
from google.oauth2 import id_token
from google.auth.transport import requests
# models
from app.models.users import Users
# 處理圖檔儲存
import os
import urllib.request
# schemas
from ..schemas.users_schema import UsersSchema
from marshmallow import ValidationError
# utils
from .utils import google_log_in


class UsersApi (Resource):
    def get(self):
        """
        確認使用者登入
        - 預設參數: login_status: 0, url: login_page
        - 讀取前端的資料
        - 驗證google token
        - 回傳login_status, username, user_image_url
        """
        # 預設參數
        response = {
            'login_status': 0,
            'url': 'http://www.stockhelper.com.tw:8080/login'
        }
        # 讀取前端的資料
        google_token = request.args.get('google_token', type=str)
        # google oauth client ID
        google_oauth_client_id = current_app.config['GOOGLE_OAUTH2_CLIENT_ID']

        # google驗證
        id_info = google_log_in(google_token, google_oauth_client_id)
        if id_info is None:
            return response, 500
        # 從table: users get data
        user = Users.query.filter_by(email=id_info['email']).first()
        # 圖片網址
        file_extension = 'jpg'
        file_name = str(user.id) + '.' + file_extension
        file_url = url_for('static', filename='upload/users/' + file_name)
        user_image_url = 'http://www.stockhelper.com.tw:8889' + file_url
        # 使用者存在，更改回傳值。
        response['login_status'] = 1
        response['username'] = user.username
        response['user_email'] = user.email
        response['user_image_url'] = user_image_url
        return response

    def post(self):
        """
        使用者登入:
        - 讀取前端的資料
        - 驗證google token
        - 驗證資料
        - 回傳index url, username, user_image_url
        """
        # 上傳資料夾路徑: static/upload/users/<file>
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'users/')
        # google oauth client ID
        google_oauth_client_id = current_app.config['GOOGLE_OAUTH2_CLIENT_ID']
        # 讀取前端資料
        token = request.json['id_token']
        # google驗證
        try:
            # Specify the GOOGLE_OAUTH2_CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                google_oauth_client_id
            )
            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            # reference: https://developers.google.com/identity/sign-in/web/backend-auth
        except ValueError:
            # Invalid token
            raise ValueError('Invalid token')

        # 驗證資料
        data = {
            'username': id_info['name'],
            'email': id_info['email']
        }
        try:
           validated_data = UsersSchema().load(data)
        except ValidationError as error:
            print("ERROR: data is invalid")

        # email若不存在DB，新增；
        user = Users.query.filter_by(email=validated_data['email']).first()
        if user is None:
            user = Users.create(**validated_data)

        # 圖片進入資料庫
        image_url = id_info['picture']
        file_extension = 'jpg'
        file_name = str(user.id) + '.' + file_extension
        urllib.request.urlretrieve(image_url, os.path.join(upload_folder, file_name))

        return {
            'url': 'http://www.stockhelper.com.tw:8080/',
        }

