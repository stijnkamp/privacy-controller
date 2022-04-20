import configparser
import sqlite3
CONFIG_PATH = "/etc/pihole/pihole-FTL.conf"
def getPiHoleConf():
    config = configparser.ConfigParser()
    with open(CONFIG_PATH, 'r') as f:
        config_string = '[DEFAULT]\n' + f.read()
    print(config_string)
    config.read_string(config_string)
    return config

def get_database_file():
    config = getPiHoleConf()
    if('DBFILE' in config): 
        return config['DBFILE']
    else:
        return "/etc/pihole/pihole-FTL.db"