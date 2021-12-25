# UMLS-Graph

Build a medical knowledge graph based on Unified Language Medical System (UMLS)

## Requisite

Install MySQL Server 5.6 and import UMLS data into MySQL database. Please refer to [UMLS](https://www.nlm.nih.gov/research/umls/index.html) websites on how to install the UMLS database. 

## Installation

```pip
pip install umls-graph
```

## Let Codes Speak

```python
from umls_graph.dataset import make_umls_all

# MySQL database information
mysql_info = {}
mysql_info["database"] = "umls"
mysql_info["username"] = "root"
mysql_info["password"] = "{not gonna tell you}"
mysql_info["hostname"] = "localhost"

# read all UMLS table and save them to csv formatted files in a specific folder
make_umls_all(mysql_info=mysql_info,save_folder="umls_datasets")

```

## License
The `umls-graph` project is provided by [Donghua Chen](https://github.com/dhchenx/umls-graph). 

NOTE: This project DOES NOT provide the UMLS data download due to the license issue. In addition, the processed data are not verified in actual clinical use.  Please be response for any UMLS data use. 