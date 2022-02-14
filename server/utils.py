import configparser
import os


def get_config():
    config = configparser.ConfigParser()
    config.read(get_config_path())
    return config


def get_config_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return f"{dir_path}/{'server.ini'}"