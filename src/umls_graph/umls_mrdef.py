#!/usr/bin/python3

import pymysql
import os

def make_umls_mrdef(mysql_info,save_path_rels="umls_def_rels.csv",save_path_nodes="umls_def_nodes.csv",save_folder=""):
    if save_folder!="":
        save_path_rels=os.path.join(save_folder,save_path_rels)
        save_path_nodes = os.path.join(save_folder, save_path_nodes)
    if os.path.exists(save_path_rels):
        print(f"{save_path_rels} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * from mrdef"
    sql_count = "SELECT count(*) from mrdef"

    # write file
    header = ":START_ID,:END_ID,:TYPE\n"
    header_n = ":ID,:LABEL,CUI,AUI,ATUI,SATUI,SAB,DEF,SUPPRESS,CVF\n"

    fo = open(save_path_rels, 'w', encoding='utf-8')
    fo_n = open(save_path_nodes, 'w', encoding='utf-8')

    cursor.execute(sql_count)
    count = cursor.fetchone()[0]
    batch_size = 20 * 10000  # whatever

    print("total record count: " + str(count))

    counter = 0
    fo.write(header)
    fo_n.write(header_n)
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
            AUI = row[list_cols.index('AUI')]
            ATUI = row[list_cols.index('ATUI')]
            SATUI = row[list_cols.index('SATUI')]
            SAB = row[list_cols.index('SAB')]
            DEF = row[list_cols.index('DEF')].replace("\"", "'")
            SUPPRESS = row[list_cols.index('SUPPRESS')]
            CVF = row[list_cols.index('CVF')]

            if SUPPRESS == None:
                SUPPRESS = ""
            if CVF == None:
                CVF = ""
            if SATUI == None:
                SATUI = ""

            # print results
            line = str(AUI) + "," + str(ATUI) + ",\"" + str("DEF") + "\""
            # +str(ATUI)+"\",\""+str(SATUI)+"\",\""+SAB+"\",\""+ATV.replace('\"',"'")+"\",\""+str(SUPPRESS)+"\",\""+str(CVF)+"\""
            # print(line)
            fo.write(line + "\n")

            line2 = str(ATUI) + "," + str("Definition") + ",\"" + str(CUI) + "\",\"" + str(AUI) + "\",\"" + str(
                ATUI) + "\",\"" + str(SATUI) + "\",\"" + str(SAB) + "\",\"" + str(DEF) + "\",\"" + str(
                SUPPRESS) + "\",\"" + str(CVF) + "\""
            fo_n.write(line2 + "\n")

            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()
    fo_n.close()

    # close connection
    db.close()