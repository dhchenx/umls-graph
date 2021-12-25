#!/usr/bin/python3

import pymysql
import os
def make_umls_mrrel(mysql_info,save_path="umls_rels.csv",save_folder=""):
    if save_folder!="":
        save_path=os.path.join(save_folder,save_path)
    if os.path.exists(save_path):
        print(f"{save_path} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * from mrrel"
    sql_count = "SELECT count(*) from mrrel"

    # write file
    header = ":START_ID,:END_ID,:TYPE,RELA,RUI,SAB,SL,RG,STYPE1,STYPE2,SRUI,SUPPRESS,CVF\n"

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
            CUI1 = row[list_cols.index('CUI1')]
            CUI2 = row[list_cols.index('CUI2')]
            AUI1 = row[list_cols.index('AUI1')]
            AUI2 = row[list_cols.index('AUI2')]
            STYPE1 = row[list_cols.index('STYPE1')]
            STYPE2 = row[list_cols.index('STYPE2')]
            start_node = CUI1
            end_node = CUI2
            if STYPE1 == 'AUI':
                start_node = AUI1
            if STYPE2 == 'AUI':
                end_node = AUI2
            if AUI1 == None:
                start_node = CUI1
            if AUI2 == None:
                end_node = CUI2

            REL = row[list_cols.index('REL')]
            RELA = row[list_cols.index('RELA')]
            RUI = row[list_cols.index('RUI')]
            SAB = row[list_cols.index('SAB')]
            SL = row[list_cols.index('SL')]
            RG = row[list_cols.index('RG')]

            SRUI = row[list_cols.index('SRUI')]
            SUPPRESS = row[list_cols.index('SUPPRESS')]
            CVF = row[list_cols.index('CVF')]

            if SRUI == None:
                SRUI = ""
            if SUPPRESS == None:
                SUPPRESS = ""
            if CVF == None:
                CVF = ""

            if SAB == None:
                SAB = ""
            if RUI == None:
                RUI = ""
            if REL == None:
                REL = ""
            if SL == None:
                SL = ""
            if RG == None:
                RG = ""
            if RELA == None:
                RELA = ""

            # print results
            line = str(start_node) + "," + str(end_node) + ",\"" + str(REL) + "\",\"" + str(RELA) + "\",\"" + str(
                RUI) + "\",\"" + str(SAB) + "\",\"" + str(SL) + "\",\"" + \
                   RG + "\",\"" + STYPE1 + "\",\"" + STYPE2 + "\",\"" + str(SRUI) + "\",\"" + str(
                SUPPRESS) + "\",\"" + str(CVF) + "\""
            # print(line)
            fo.write(line + "\n")
            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()

    # close connection
    db.close()