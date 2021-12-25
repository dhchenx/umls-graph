#!/usr/bin/python3

import pymysql
import os

def make_umls_mrsty(mysql_info,save_path="umls_sty_rels.csv",save_folder=""):
    if save_folder!="":
        save_path=os.path.join(save_folder,save_path)
    if os.path.exists(save_path):
        print(f"{save_path} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * from mrsty"
    sql_count = "SELECT count(*) from mrsty"

    # write file
    header = ":START_ID,:END_ID,:TYPE,CUI,TUI,STN,STY,ATUI,CVF\n"

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
            TUI = row[list_cols.index('TUI')]
            STN = row[list_cols.index('STN')]
            STY = row[list_cols.index('STY')].replace("\"", "'")
            ATUI = row[list_cols.index('ATUI')]
            CVF = row[list_cols.index('CVF')]

            if CVF == None:
                CVF = ""

            # print results
            line = str(CUI) + "," + str(TUI) + ",\"" + str("HAS_SR") + "\",\"" + str(CUI) + "\",\"" + str(
                TUI) + "\",\"" + str(STN) + "\",\"" + str(STY) + "\",\"" + \
                   str(ATUI) + "\",\"" + str(CVF) + "\""
            # print(line)
            fo.write(line + "\n")
            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()

    # close connection
    db.close()