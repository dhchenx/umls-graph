# Import UMLS into UMKG

This document illustrates principles and steps of importing core data structures of UMLS into the UMKG database. 

## Step 1: Install the UMLS database

First, we need to follow guideline of UMLS to setup MySQL 5.6 server for convenience of fetching UMLS concepts, strings, atoms and their relationships.

The steps of loading UMLS knowledge sources:
1. Download UMLS's 2020AB release files in the following [link](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html).
2. Unzip the UMLS release files and then also unzip `mmsys.zip` into the current folder. 
3. click `run64.bat` to run MetamorphoSys for customizing your UMLS subset and browse the details of UMLS concepts. 
4. Then we turn to the subset folder exported by MetamorphoSys and check if there is mysql scripts created in the `META` folder. If so, we are ready to import such scripts and data into MySQL 5.6 server. 

The steps of setting up MySQL 5.6 for storing UMLS knowledge sources:
1. Download [MySQL 5.6](https://dev.mysql.com/downloads/mysql/5.6.html) from Oracle website and install MySQL server by default settings of MySQL installation. Then we get the MySQL 5.6 running. 
2. For convenience of browsing data, we also install [MySQL WorkBench](https://dev.mysql.com/downloads/workbench/) to have GUI for operating MySQL database's data. 
3. Before running this script file, we need to create a schema or database inside the MySQL database server. Turn to the `META` folder that contains mysql script file `populate_mysql_db.bat` and change MySQL login information (db user,db password, db name) inside the `bat` file. 
4. Then, we run the `populate_mysql_db.bat` and wait for its completion. 
5. Finally, we got entire datasets of UMLS stored in MySQL 5.6 server so later we can easily fetch necessary contents from MySql server. 

![MySql for UMLS](images/umls-mysql.png)

## Step 2: Run scripts to obtain UMLS data structures

Then we write Python scripts to obtain UMLS core structures and store the fetched data into CSV format of importing graph databases.

In this case, we ignore the procedure of setting up Python environment, which can be easily found online. 

With proper settings of Python environment and the installed PyCharm, we can simply write Python scripts to obtain key information from the UMLS database running on MySQL server.

Here is the example of accessing the UMLS database:

```python
#!/usr/bin/python3
import pymysql

db = pymysql.connect("localhost", "[YOUR DB USERNAME]", "[YOUR DB PASSWORD]", "umls2020")
cursor = db.cursor()
sql = "SELECT * from mrconso limit 1,100"
cursor.execute(sql)
results = cursor.fetchall()

# obtain a list of column names
cols=cursor.description
list_cols = []
for i in range(len(cols)):
    list_cols.append(cols[i][0])
print(list_cols)

for row in results:
    # ID
    AU = row[list_cols.index('AUI')]
    # Relationships
    CUI = row[list_cols.index('CUI')]
    LUI = row[list_cols.index('LUI')]
    SUI = row[list_cols.index('SUI')]
    # Properties
    STR = row[list_cols.index('STR')]
    # print results
    print(CUI+"\t"+LUI+"\t"+SUI+"\t"+STR)
# close connection
db.close()
```

Because UMLS contains complicated data structures to represent concepts, terms, strings, atoms, and their relationships. For better understanding of these concepts and structures, I highly recommend you reading the [UMLS Reference Manual](https://www.ncbi.nlm.nih.gov/books/NBK9676/). 

Here follows key UMLS structures to obtain:

### (1) Concepts, Terms, Strings, and Atoms

We use the `mmrconso` table to obtain following information. 

1. we retrieve distinct CUIs for representing ```Concept``` nodes. 
2. we retrieve distinct LUIs for representing ```Term``` nodes.
3. we retrieve distinct SUIs for representing ```String``` nodes.
4. we retrieve distinct AUIs and their properties for representing ```Atom``` nodes.

Thus, we get the nodes CSV file. 

### (2) Relationships between Concepts, Terms, Strings, and Atoms

We use the `mrrel` table to obtain the above entities' relationships and properties of relationship.

Source node ID is obtained from CUI1 or AUI1 fields in the table;
Target node ID is obtained from CUI2 or AUI2 fields in the table. 

The we create relationship between CUI1/AUI1 and CUI2/AUI2 and attach the rest of properties of relationship into the created relationship. 

Thus, we get the relationship CSV file.

### (3) Mapping Relationships

To do...

### (4) Definitions

To do...

### (5) Attributes

To do...

After we follow the aforementioned steps to obtain necessary information, the we are ready for importing UMLS data into the Neo4j database. 


## Step 3: Import UMLS data into UMKG

After we prepare all datasets from UMLS, then we execute Neo4j-admin import command to batch import UMLS data into the UMKG dataset we created in Neo4j Desktop. 

The Neo4j-Admin import Command can be useful for importing large amount of graph data into the database. 

Please follow the below steps: 
1. Move the created datasets in the `import` folder in the Neo4j database root folder. 
2. Open Windows Command Program (cmd.exe) and change root folder to the database root folder, which the parent folder of `bin` folder containing the `neo4j-admin.bat` file. 
3. Enter the example importing scripts as follows:

```
"bin/neo4j-admin.bat" import --nodes "import/umls_aui_nodes.csv"  --nodes "import/umls_cui_nodes.csv" --nodes "import/umls_lui_nodes.csv" --nodes "import/umls_sui_nodes.csv" --relationships "import/umls_rels.csv" --database UMLS.db
```

In the above script, `--nodes` represents specifying location of node tables used, and `--relationships` represents specifying location of relationship tables. You can specify multiple nodes or relationships table for importing various types of nodes and relationships. 

![MySql for UMLS](images/umls-mysql-import.png)

Please look for more information from [Neo4j Manual](https://neo4j.com/graphacademy/training-intro-40/19-using-neo4j-admin-tool-import/). 

After we execute the script and anything is prepared correctly, then we can get the UMLS data into the Neo4j database. 

## Step 4: Query test

After we finish importing UMLS data, we can use simple query statements to examine whether the imported data are correctly stored and organized. 

![MySql for UMLS](images/umls-neo4j.png)

