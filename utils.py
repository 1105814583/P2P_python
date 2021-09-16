import json

import pymysql
from bs4 import BeautifulSoup

import app


def assert_pubilc(self, response, status_code, status, description):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertIn(description, response.json().get("description"))


def third_openAccoun_interface(response, session):
    html_data = response.json().get("description").get("form")
    soup = BeautifulSoup(html_data, "html.parser")
    # soup = BeautifulSoup (html_data, "html.parser")
    # 提取url
    action_url = soup.form["action"]
    # 提取input标签数据
    data = {}
    for input_data in soup.find_all("input"):
        name = input_data["name"]
        value = input_data["value"]
        data.update({name: value})

    response = session.post(action_url, data=data)
    return response


# 读取文件内容及参数
# filename 文件名：类型为str
# parameter_name_list 参数列表 列表参数为str 比如["xx","xx"]

def read_data_parameter(filename, parameter_name_list):
    # 生成文件路路径
    file = app.BASE_DIR + "/data/" + filename
    # 读取文件
    with open(file, encoding="UTF-8")as f:
        data_list = json.load(f)
    # 定义参数化列表
    parameter_list = []
    # 读取每组数据的值并添加到定义的参数化列表中
    for data in data_list:
        name_list = []
        for parameter_name in parameter_name_list:
            name_list.append(data.get(parameter_name))
        parameter_list.append(name_list)
    return parameter_list


def clear_data():
    # 建议游标
    conn = pymysql.connect(host=app.MYSQL_HOST, user=app.MYSQL_USER, password=app.MYSQL_PASSWORD,
                           database=app.MYSQL_MENBER, port=app.MYSQL_PORT)
    # 生成游标
    cursor = conn.cursor()
    # 执行sql
    sql1 = "delete from mb_member_register_log where phone in ('13710733730','13710733731','13088881132','13088881133','13088881134');"
    sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13710733730','13710733731','13710733732','13710733733','13088881134');"
    sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13710733730','13710733731','13710733732','13710733733','13710733734');"
    sql4 = "delete from mb_member WHERE phone in ('13710733730','13710733731','13710733732','13710733733','13710733734');"
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("事务处理失败", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
