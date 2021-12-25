from umls_graph.umls_ambiglui import *
from umls_graph.umls_ambigsui import *
from umls_graph.umls_mrconso import *
from umls_graph.umls_mrconso_concept import *
from umls_graph.umls_mrconso_string import *
from umls_graph.umls_mrconso_term import *
from umls_graph.umls_mrdef import *
from umls_graph.umls_mrrel import *
from umls_graph.umls_mrsat import *
from umls_graph.umls_mrsmap import *
from umls_graph.umls_mrsty import *
from umls_graph.umls_srdef import *

def make_umls_all(save_folder,mysql_info=None):
    if mysql_info==None:
        mysql_info = {}
        mysql_info["database"] = "umls"
        mysql_info["username"] = "root"
        mysql_info["password"] = "123456"
        mysql_info["hostname"] = "localhost"

    make_umls_ambiglui(mysql_info,save_folder=save_folder)
    make_umls_ambigsui(mysql_info, save_folder=save_folder)
    make_umls_mrconso(mysql_info, save_folder=save_folder)
    make_umls_mrconso_concept(mysql_info, save_folder=save_folder)
    make_umls_mrconso_string(mysql_info, save_folder=save_folder)
    make_umls_mrconso_term(mysql_info, save_folder=save_folder)
    make_umls_mrdef(mysql_info,save_folder=save_folder)
    make_umls_mrrel(mysql_info, save_folder=save_folder)
    make_umls_mrsat(mysql_info, save_folder=save_folder)
    make_umls_mrsmap(mysql_info, save_folder=save_folder)
    make_umls_mrsty(mysql_info, save_folder=save_folder)
    make_umls_srdef(mysql_info, save_folder=save_folder)


