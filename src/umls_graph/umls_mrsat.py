#!/usr/bin/python3

import pymysql
import os

def make_umls_mrsat(mysql_info,save_path_rels="umls_rels.csv",save_path_nodes="umls_atui_nodes.csv",save_folder=""):
    if save_folder!="":
        save_path_rels=os.path.join(save_folder,save_path_rels)
        save_path_nodes = os.path.join(save_folder, save_path_nodes)
    if os.path.exists(save_path_rels):
        print(f"{save_path_rels} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * from mrsat"
    sql_count = "SELECT count(*) from mrsat"

    # write file
    header = ":START_ID,:END_ID,:TYPE\n"
    header_n = ":ID,:LABEL,ATUI,SATUI,ATN,SAB,ATV,SUPPRESS,CVF\n"

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
            LUI = row[list_cols.index('LUI')]
            SUI = row[list_cols.index('SUI')]
            METAUI = row[list_cols.index('METAUI')]
            STYPE = row[list_cols.index('STYPE')]
            CODE = row[list_cols.index('CODE')]
            ATUI = row[list_cols.index('ATUI')]
            SATUI = row[list_cols.index('SATUI')]
            ATN = row[list_cols.index('ATN')]
            SAB = row[list_cols.index('SAB')]
            ATV = row[list_cols.index('ATV')].replace("\"", "'")
            SUPPRESS = row[list_cols.index('SUPPRESS')]
            CVF = row[list_cols.index('CVF')]

            start_node = CUI
            if STYPE == 'CUI':
                start_node = CUI
            if STYPE == "AUI" or STYPE == "RUI" or STYPE == "SDUI" or STYPE == "SCUI":
                start_node = METAUI
            if STYPE == "CODE":
                start_node = CODE

            end_node = ATUI

            if CVF == None:
                CVF = ""
            if SUPPRESS == None:
                SUPPRESS = ""
            if SATUI == None:
                SATUI = ""

            # print results
            line = str(start_node) + "," + str(end_node) + ",\"" + str(ATN) + "\""
            # +str(ATUI)+"\",\""+str(SATUI)+"\",\""+SAB+"\",\""+ATV.replace('\"',"'")+"\",\""+str(SUPPRESS)+"\",\""+str(CVF)+"\""
            # print(line)
            fo.write(line + "\n")

            line2 = str(ATUI) + "," + str("Attribute") + ",\"" + str(ATUI) + "\",\"" + str(SATUI) + "\",\"" + str(
                ATN) + "\",\"" + str(SAB) + "\",\"" + str(ATV) + "\",\"" + str(SUPPRESS) + "\",\"" + str(CVF) + "\""
            fo_n.write(line2 + "\n")

            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()
    fo_n.close()

    # close connection
    db.close()