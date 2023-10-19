import pymysql
from flask import Flask, render_template, request
import timer

sensor_db = pymysql.connect(
    user='root', 
    passwd='1234', 
    host='127.0.0.1', 
    db='air', 
    charset='utf8'
)

#cursor = sensor_db.cursor(pymysql.cursors.DictCursor)
cursor = sensor_db.cursor()

#sql = "DELETE FROM sensor WHERE _id = 2;"
sql = "SELECT * FROM airline"


cursor.execute(sql)


data_list = cursor.fetchall()


#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
    
    sql = "SELECT * from airline"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    
    
    return render_template('html.html',data_list=data_list)
    
if __name__=="__main__":
    #app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    app.run(host="127.0.0.1", port="80", debug=True)