
import pymysql
def insert_customer(name, email, tall, birthday):
    sql = "insert into customer (name, email, tall, birthday, created_at) \
             values (%s, %s, %s, %s, now())"
    with pymysql.connect(host="127.0.0.1", port=3306, user="playdata", password="1111", db='mydb') as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, [name, email, tall, birthday])
            conn.commit()
    return result

def update_customer(cust_id, name, email, tall, birthday):
    sql = "update customer set name=%s, email=%s, tall=%s, birthday=%s where id=%s"
    with pymysql.connect(host="127.0.0.1", port=3306, user="playdata", password="1111", db='mydb') as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, [name, email, tall, birthday, cust_id])
            conn.commit()
    return result

def delete_customer_by_id(cust_id):
    sql = "delete from customer where id=%s"
    with pymysql.connect(host="127.0.0.1", port=3306, user="playdata", password="1111", db='mydb') as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, [cust_id])
            conn.commit()
    return result

def delete_customer_by_name(name):
    sql = "delete from customer where name = %s"
    with pymysql.connect(host="127.0.0.1", port=3306, user="playdata", password="1111", db='mydb') as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, [name])
            conn.commit()
    return result

def select_customer_by_id(cust_id):
    sql = "select * from customer where id = %s"  # PK 조건으로 조회: 결과행 - 1행. => fetechone()
    with pymysql.connect(host="127.0.0.1", port=3306, user="playdata", password="1111", db='mydb') as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, [cust_id])
            return cursor.fetchone()

def select_customer_by_name(name):
    # 조회조건이 unique 하지 않은 컬럼: 결과행: 0 ~ N행. => fetchall()
    sql = "select * from customer where name = %s" 
    with pymysql.connect(host="127.0.0.1", port=3306, user="playdata", password="1111", db='mydb') as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, [name])
            return cursor.fetchall()

def select_customer_by_tall_range(start_tall, stop_tall):
    sql = "select * from customer where tall between %s and %s"
    with pymysql.connect(host="127.0.0.1", port=3306, user="playdata", password="1111", db='mydb') as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, [start_tall, stop_tall])
            return cursor.fetchall()
