# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 16:28
# @Author  : play4fun
# @File    : read_db_parse.py
# @Software: PyCharm

"""
read_db_parse.py:
"""
import sqlite3
import synonyms, random
from datetime import datetime


def isNum(word):
    try:
        return word.encode('ascii').isnum()
    except UnicodeEncodeError:
        return False


def sqlite_dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def fix_4_options(item: dict):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    answer = item['OPTION']
    answer = answer.strip()
    if answer.isnumeric():
        anint = int(answer)
        options = random.choices(range(anint - 50, anint + 50), k=5)
    else:
        xl = synonyms.nearby(answer)
        options = xl[0][:6]

        if len(options) == 0:
            print('Error:不存在')#TODO out of vocabulary 词库不够大
        else:
            if answer != options[0]:
                print('致命错误')
            options = options[1:]

    print(options)
    if len(options) == 5:
        sql = f'INSERT INTO PUZZLES (`question`,`opt1`,`opt2`,`opt3`,`opt4`,`opt5`,`answer`,`type`,`create_time`) VALUE ("{item["QUIZ"]}","{options[0]}","{options[1]}","{options[2]}","{options[3]}","{options[4]}","{answer}","{item["TYPE"]}","{now}")'  # TODO
        print(sql)
    print('------------')


def main():
    db_path = '数据库/智力答题-题库data.db'
    # 链接sqlite数据库
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite_dict_factory
    cursor = conn.cursor()

    #
    sql = 'SELECT QUIZ,OPTION,TYPE FROM QUSTION LIMIT 1000'
    cursor.execute(sql)
    rs = cursor.fetchall()
    # print(rs)

    #
    for item in rs[200:400]:
        print(item)
        fix_4_options(item)


if __name__ == '__main__':
    main()
