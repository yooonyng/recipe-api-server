from hashlib import pbkdf2_hmac
from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
from email_validator import validate_email, EmailNotValidError
from passlib.hash import pbkdf2_sha256

from utils import hash_password

class UserRegisterResource(Resource):
    def post(self):

        # {
        # "username":"홍길동",
        # "email":"abc@naver.com",
        # "password":"1234"
        # }

        # 1. 클라이언트가 body에 보내준 json을 받아온다.
        data = request.get_json()

        # 2. 이메일 주소 형식이 제대로 된 주소 형식인지 확인하는 코드
        # DB에 저장하지 않고 테스트 코드만 작성해보기
        try :
            validate_email(data['email'])

        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            return {'error':str(e)}, 400

        # 3. 비밀번호의 길이가 유효한지 체크한다.
        # 비밀번호 길이는 4자리 이상 12자리 이하로 한다.
        if len(data['password']) < 4 or len(data['password']) > 12:
            return {'error':'비밀번호길이를확인하세요'}, 400

        # 4. 비밀번호를 암호화한다.
        # data['password']

        hashed_password = hash_password(data['password'])
        print(hashed_password)

        # 5. 데이터베이스에 회원정보를 저장한다.
        

        

        return