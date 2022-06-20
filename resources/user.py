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
        try:
            # 데이터 insert
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into user
                        (username,email,password)
                        values
                        (%s,%s,%s);'''

            record = (data['username'],data['email'],hashed_password)
            
            # 3. 커서를 가져온다
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다
            cursor.execute(query,record)

            # 5. 커넥션을 커밋해줘야한다 -> DB에 영구적으로 반영하기
            connection.commit()

            # 5-1. DB에 저장된 아이디값 가져오기
            user_id = cursor.lastrowid

            # 6. 자원 해제
            cursor.close()
            connection.close()


        except mysql.connector.Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"error":str(e)}, 503

        return {"result":"success","user_id":user_id}, 200
