# PyMySQL (100 % Python, pas de compilation C) se fait passer pour mysqlclient.
# C'est le choix le plus sûr pour un runtime WebAssembly/WASIX comme Wasmer.
import pymysql

pymysql.install_as_MySQLdb()
