import configparser
import re


class configReader:
    def __init__(self):
        print("""
----------------------------------------------------------------------------------------------------
Reading config file ...
        """)
        config = configparser.ConfigParser()
        config.read('./grading.ini')
        self.path = config.get('PATH','path')
        self.mode = config.getint('GRADING','mode')
        self.res_rate = config.getfloat('GRADING','res_rate')
        self.none_clone_rate = config.getfloat('GRADING','none_clone_rate')
        self.style_rate = config.getfloat('GRADING','style_rate')
        self.is_sort = config.getboolean('GRADING','is_sort')

        self.minTokens = [int(i) for i in re.findall('\d+',config['CLONE']['minTokens'])]
        self.stride = [int(i) for i in re.findall('\d+',config['CLONE']['stride'])]
        self.similarity = [float(i) for i in re.findall('\d+\.?\d*',config['CLONE']['similarity'])]
        self.distance = [float(i) for i in re.findall('\d+\.?\d*',config['CLONE']['distance'])]
        self.diff = config.getfloat('CLONE','diff')
        self.is_score = config.getboolean('CLONE','is_score')

        self.is_remove = config.getboolean('REMOVE','is_remove')