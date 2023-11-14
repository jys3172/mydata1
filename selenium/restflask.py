from flask import Flask, jsonify
import pymysql.cursors  # 수정된 부분
import pymysql
from restdata import crawl_and_store_information
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL 설정
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'AIR'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # MySQL 호스트

# 크롤링 및 MySQL 데이터베이스에서 데이터 가져오기
def fetch_data_from_db():
    try:
        crawl_and_store_information()

        connection = pymysql.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            database=app.config['MYSQL_DATABASE_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM rest")  # 적절한 테이블 이름으로 변경
            data = cursor.fetchall()

    except Exception as e:
        return str(e)

    finally:
        if connection is not None:
            connection.close()

    return data

# API 엔드포인트 정의
@app.route('/api/get_informatons', methods=['GET'])
def get_data():
    # 크롤링 및 MySQL 데이터베이스에서 데이터 가져오기
    data = fetch_data_from_db()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)