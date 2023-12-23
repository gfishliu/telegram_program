import mysql.connector
from datetime import date, timedelta
from loguru import logger

# MySQLサーバーへの接続設定
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# カーソルの作成
mycursor = mydb.cursor()

def select_login(personal_id):
    check_user_query = "SELECT * FROM login_info WHERE personal_id = %s"
    logger.info(f'select_login:{check_user_query}')
    mycursor.execute(check_user_query, [personal_id])
    user_record = mycursor.fetchone()
    return user_record


def update_login_referee(personal_id, referee_id):
    sql_update = "UPDATE login_info SET referee_id = %s WHERE personal_id = %s"
    val_update = [referee_id, personal_id]
    logger.info(f'update_login_referee:{val_update}')
    mycursor.execute(sql_update, val_update)
    mydb.commit()


def update_login_expirydate(personal_id, expiry_date):
    sql_update = "UPDATE login_info SET expiry_date = %s WHERE personal_id = %s"
    val_update = [expiry_date, personal_id]
    logger.info(f'update_login_expirydata:{val_update}')
    mycursor.execute(sql_update, val_update)
    mydb.commit()


def insert_login(personal_id):
    # データ挿入
    sql_insert = "INSERT INTO login_info (personal_id, referee_id, login_date, expiry_date, whitelist) VALUES (%s, %s, %s, %s, %s)"
    val_insert = [personal_id, 0, date.today(), date.today()+timedelta(days=2), "No"]
    mycursor.execute(sql_insert, val_insert)
    mydb.commit()
    #print(mycursor.rowcount, "レコード挿入完了。")

def insert_privatekey(personal_id, private_key):
    # データ挿入
    sql_insert = "INSERT INTO personal_key (personal_id, private_key) VALUES (%s, %s)"
    val_insert = [personal_id, private_key]
    mycursor.execute(sql_insert, val_insert)
    mydb.commit()
    #print(mycursor.rowcount, "レコード挿入完了。")





"""
# データの削除
sql_delete = "DELETE FROM 表名 WHERE 条件"
mycursor.execute(sql_delete)
mydb.commit()
print(mycursor.rowcount, "レコード削除完了。")

# データの更新
sql_update = "UPDATE 表名 SET 列1 = %s WHERE 条件"
val_update = ("新しい値",)
mycursor.execute(sql_update, val_update)
mydb.commit()
print(mycursor.rowcount, "レコード更新完了。")
"""
"""
login(1234543)
# データの検索
sql_select = "SELECT * FROM login_info"
mycursor.execute(sql_select)
result = mycursor.fetchall()
for row in result:
    print(row)
"""
# 接続をクローズ
#mydb.close()

