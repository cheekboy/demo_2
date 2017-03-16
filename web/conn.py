#!/usr/bin/env python
# coding:utf-8

#!/usr/bin/env python
# coding:utf-8
import MySQLdb
import logging

def writeDb(sql,db_data=()):
    """
    连接mysql数据库（写），并进行写的操作
    """
    try:
        conn = MySQLdb.connect(db='reboot',user='root',passwd='123456',host='127.0.0.1',port=3306,charset="utf8")
        cursor = conn.cursor()
    except Exception,e:
        print e
        logging.error('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        conn.commit()
    except Exception,e:
        conn.rollback()
        logging.error('数据写入失败:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return True