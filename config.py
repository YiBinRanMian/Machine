import configparser
import re


class configReader:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./grading.ini')
        self.path = config.get('PATH','path')
        self.mode = config.getint('GRADING','mode')
        self.is_sort = config.getboolean('GRADING','is_sort')

        self.minTokens = [int(i) for i in re.findall('\d+',config['CLONE']['minTokens'])]
        self.stride = [int(i) for i in re.findall('\d+',config['CLONE']['stride'])]
        self.similarity = [float(i) for i in re.findall('\d+\.?\d*',config['CLONE']['similarity'])]
        self.distance = [float(i) for i in re.findall('\d+\.?\d*',config['CLONE']['distance'])]
        self.diff = config.getfloat('CLONE','diff')

