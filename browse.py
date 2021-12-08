import pymysql

conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='user1',
                       passwd='12345',
                       db='member_db')  #連接資料庫
cursor = conn.cursor()
sqlstr = 'SELECT * FROM login'  #讀取登入資料表
cursor.execute(sqlstr)
rows = cursor.fetchall()  #取得登入資料
print('%-15s %-20s' % ('帳號','登入時間'))
print('=============== ====================')
for row in rows:
    print('%-15s %-20s' % (row[0], row[1]))

conn.close()