#!/usr/bin/python3

import pymysql
import os

def make_umls_ambigsui(mysql_info,save_path="umls_ambig_sui.csv",save_folder=""):
    if save_folder!="":
        save_path=os.path.join(save_folder,save_path)
    if os.path.exists(save_path):
        print(f"{save_path} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * from ambigsui"
    sql_count = "SELECT count(*) from ambigsui"

    # write file
    header = ":START_ID,:END_ID,:TYPE,SUI,CUI\n"

    fo = open(save_path, 'w', encoding='utf-8')

    cursor.execute(sql_count)
    count = cursor.fetchone()[0]
    batch_size = 20 * 10000  # whatever

    counter = 0
    fo.write(header)
    for offset in range(0, count, batch_size):
        cursor.execute(sql + " LIMIT %s OFFSET %s", (batch_size, offset))

        # obtain a list of column names
        cols = cursor.description
        list_cols = []
        for i in range(len(cols)):
            list_cols.append(cols[i][0])
        # print(list_cols)

        for row in cursor:
            # ID
            CUI = row[list_cols.index('CUI')]
            SUI = row[list_cols.index('SUI')]

            # print results
            line = str(SUI) + "," + str(CUI) + ",\"" + str("AMBIGSUI") + "\",\"" + SUI + "\",\"" + CUI + "\""
            # print(line)
            fo.write(line + "\n")
            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()

    # close connection
    db.close()

if __name__=="__main__":
    mysql_info = {}
    mysql_info["database"] = "umls"
    mysql_info["username"] = "root"
    mysql_info["password"] = "123456"
    mysql_info["hostname"] = "localhost"
    make_umls_ambigsui(mysql_info,"../../examples/umls_datasets/umls_ambig_sui.csv")
