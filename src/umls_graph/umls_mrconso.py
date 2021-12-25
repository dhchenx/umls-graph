#!/usr/bin/python3

import pymysql
import os

def make_umls_mrconso(mysql_info,save_path="umls_aui_nodes.csv",save_folder=""):
    if save_folder!="":
        save_path=os.path.join(save_folder,save_path)
    if os.path.exists(save_path):
        print(f"{save_path} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * from mrconso"
    sql_count = "SELECT count(*) from mrconso"

    # write file
    header = ":ID,:LABEL,SAB,CUI,LUI,SUI,STR,AUI,TTY,CODE,SRL,SUPPRESS,CVF,SAUI,SCUI,SDUI,ISPREF,LAT,TS\n"

    fo = open(save_path, 'w', encoding='utf-8')

    cursor.execute(sql_count)
    count = cursor.fetchone()[0]
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
            ID = row[list_cols.index('AUI')]
            # Label
            SAB = row[list_cols.index('SAB')]
            label = "Atom"

            # Properties
            CUI = row[list_cols.index('CUI')]
            LUI = row[list_cols.index('LUI')]
            AUI = row[list_cols.index('AUI')]
            SUI = row[list_cols.index('SUI')]
            TTY = row[list_cols.index('TTY')]
            CODE = row[list_cols.index('CODE')]
            SRL = row[list_cols.index('SRL')]
            SUPPRESS = row[list_cols.index('SUPPRESS')]
            CVF = row[list_cols.index('CVF')]
            SAUI = row[list_cols.index('SAUI')]
            SCUI = row[list_cols.index('SCUI')]
            SDUI = row[list_cols.index('SDUI')]
            ISPREF = row[list_cols.index('ISPREF')]
            LAT = row[list_cols.index('LAT')]
            TS = row[list_cols.index('TS')]

            if SAUI == None:
                SAUI = ''
            if SCUI == None:
                SCUI = ''
            if SDUI == None:
                SDUI = ''
            if TS == None:
                TS = ""
            if LAT == None:
                LAT = ""

            STR = row[list_cols.index('STR')].replace("\"", "'")

            # pring results
            line = ID + "," + label + "," + SAB + "," + CUI + "," + LUI + "," + SUI + ",\"" + STR + "\"," + AUI + ",\"" \
                   + TTY + "\",\"" + str(CODE) + "\",\"" + str(SRL) + "\",\"" + SUPPRESS + "\",\"" + str(
                CVF) + "\",\"" + str(SAUI) + "\",\"" + str(SCUI) + "\",\"" + str(SDUI) + "\",\"" + str(
                ISPREF) + "\",\"" + str(LAT) + "\",\"" + str(TS) + "\""
            # print(line)
            fo.write(line + "\n")
            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()

    # close connection
    db.close()