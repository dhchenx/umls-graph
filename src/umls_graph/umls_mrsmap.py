#!/usr/bin/python3

import pymysql
import os

def make_umls_mrsmap(mysql_info,save_path_rels="umls_smap_rels.csv",save_path_nodes="umls_smap_nodes.csv",save_folder=""):
    if save_folder!="":
        save_path_rels=os.path.join(save_folder,save_path_rels)
        save_path_nodes = os.path.join(save_folder, save_path_nodes)
    if os.path.exists(save_path_rels):
        print(f"{save_path_rels} exists!")
        return
    # open db connection
    db = pymysql.connect(host=mysql_info["hostname"], user=mysql_info["username"], password=mysql_info["password"], database=mysql_info["database"])

    cursor = db.cursor()

    sql = "SELECT * from mrsmap"
    sql_count = "SELECT count(*) from mrsmap"

    # write file
    header = ":START_ID,:END_ID,:TYPE,MAPSETCUI,MAPSETSAB,MAPID,MAPSID,FROMEXPR,FROMTYPE,REL,RELA,TOEXPR,TOTYPE,CVF\n"
    header_n = ":ID,:LABEL,EXPR,EXPR_TYPE\n"

    fo = open(save_path_rels, 'w', encoding='utf-8')
    fo_n = open(save_path_nodes, 'w', encoding='utf-8')

    cursor.execute(sql_count)
    count = cursor.fetchone()[0]
    batch_size = 20 * 10000  # whatever

    print("total record count: " + str(count))

    dict_expr = {}

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

            MAPSETCUI = row[list_cols.index('MAPSETCUI')]
            MAPSETSAB = row[list_cols.index('MAPSETSAB')]
            MAPID = row[list_cols.index('MAPID')]
            MAPSID = row[list_cols.index('MAPSID')]
            FROMEXPR = row[list_cols.index('FROMEXPR')]
            FROMTYPE = row[list_cols.index('FROMTYPE')]
            REL = row[list_cols.index('REL')]
            RELA = row[list_cols.index('RELA')]
            TOEXPR = row[list_cols.index('TOEXPR')]
            TOTYPE = row[list_cols.index('TOTYPE')]
            CVF = row[list_cols.index('CVF')]

            if CVF == None:
                CVF = ""
            if MAPSID == None:
                MAPSID = ""

            # print results
            line = "\"" + str(FROMEXPR) + "\",\"" + str(TOEXPR) + "\",\"" + str("SMAP") + "\",\"" + str(
                MAPSETCUI) + "\",\"" + str(MAPSETSAB) + "\",\"" + MAPID + "\",\"" + MAPSID + "\",\"" \
                   + str(FROMEXPR) + "\",\"" + str(FROMTYPE) + "\",\"" + str(REL) + "\",\"" + str(RELA) + "\",\"" + str(
                TOEXPR) + "\",\"" + str(TOTYPE) + "\",\"" + str(CVF) + "\""
            # print(line)
            fo.write(line + "\n")

            # line2=str(FROMEXPR)+","+str("MapEntity")+",\""+str(FROMEXPR)+"\""
            # fo_n.write(line2+"\n")

            if FROMTYPE != "CUI" and not dict_expr.keys().__contains__(FROMEXPR):
                line2 = "\"" + str(FROMEXPR) + "\"," + str("MapEntity") + ",\"" + str(
                    FROMEXPR) + "\",\"" + FROMTYPE + "\""
                fo_n.write(line2 + "\n")
                dict_expr[FROMEXPR] = FROMTYPE
            if TOTYPE != "CUI" and not dict_expr.keys().__contains__(TOEXPR):
                line2 = "\"" + str(TOEXPR) + "\"," + str("MapEntity") + ",\"" + str(TOEXPR) + "\",\"" + TOTYPE + "\""
                fo_n.write(line2 + "\n")
                dict_expr[TOEXPR] = TOTYPE

            counter = counter + 1
        print('counter = ' + str(counter))

    fo.close()
    fo_n.close()

    # close connection
    db.close()