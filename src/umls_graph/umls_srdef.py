#!/usr/bin/python3

import pymysql
import os
def make_umls_srdef(mysql_info,save_path="umls_sr_nodes.csv",save_folder=""):
    if save_folder!="":
        save_path=os.path.join(save_folder,save_path)
    if os.path.exists(save_path):
        print(f"{save_path} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * FROM srdef"
    sql_count = "SELECT count(*) FROM srdef"

    # write file
    header = ":ID,:LABEL,UI,RT,STY_RL,STN_RTN,DEF,EX,UN,NH,ABR,RIN\n"

    fo = open(save_path, 'w', encoding='utf-8')

    cursor.execute(sql_count)
    count = cursor.fetchone()[0]

    print("total record count: " + str(count))

    batch_size = 10 * 10000  # whatever

    counter = 0
    fo.write(header)
    for offset in range(0, count, batch_size):
        cursor.execute(sql + " LIMIT %s OFFSET %s", (batch_size, offset))

        # obtain a list of column names
        cols = cursor.description
        list_cols = []
        for i in range(len(cols)):
            list_cols.append(cols[i][0])
        print(list_cols)

        for row in cursor:
            # ID
            RT = row[list_cols.index('RT')]
            # Label
            UI = row[list_cols.index('UI')]
            STY_RL = row[list_cols.index('STY_RL')]
            STN_RTN = row[list_cols.index('STN_RTN')]
            DEF = row[list_cols.index('DEF')].replace("\"", "'")
            EX = row[list_cols.index('EX')]
            UN = row[list_cols.index('UN')]
            NH = row[list_cols.index('NH')]
            ABR = row[list_cols.index('ABR')]
            RIN = row[list_cols.index('RIN')]
            print(row)

            if EX == None:
                EX = ""
            if UN == None or UN == 'NULL':
                UN = ""
            if NH == None:
                NH = ""
            if ABR == None:
                ABR = ""
            if RIN == None:
                RIN = ""
            if RT == None:
                RT = ""
            if STY_RL == None:
                STY_RL = ""
            if STN_RTN == None:
                STN_RTN = ""
            if DEF == None:
                DEF = ""
            if UI == None:
                UI = ""

            UN = UN.replace("\"", "'")

            # print(UI,RT,STY_RL,STN_RTN,DEF,EX,UN+","+NH+","+ABR+","+RIN)
            print(EX)

            line = UI + "," + RT + ",\"" + STY_RL + "\",\"" + STN_RTN + "\",\"" + DEF + "\",\"" + EX + "\",\"" + UN + "\",\"" + NH + "\",\"" + ABR + "\",\"" + RIN + "\""
            fo.write(line + "\n")

            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()

    # close connection
    db.close()