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
        self.path = config.get('PATH','sole_path')
        # 评分选项
        self.mode = config.getint('GRADING','mode')
        self.res_rate = config.getfloat('GRADING','res_rate')
        self.none_clone_rate = config.getfloat('GRADING','none_clone_rate')
        self.style_rate = config.getfloat('GRADING','style_rate')
        self.is_sort = config.getboolean('GRADING','is_sort')
        self.is_intersect = config.getboolean('GRADING','is_intersect')

        # CLONE: 克隆代码选项
        self.minTokens = [int(i) for i in re.findall('\d+',config['CLONE']['minTokens'])]
        self.stride = [int(i) for i in re.findall('\d+',config['CLONE']['stride'])]
        self.similarity = [float(i) for i in re.findall('\d+\.?\d*',config['CLONE']['similarity'])]
        self.distance = [float(i) for i in re.findall('\d+\.?\d*',config['CLONE']['distance'])]
        self.diff = config.getfloat('CLONE','diff')
        self.is_diff = config.getboolean('CLONE','is_diff')
        self.is_score = config.getboolean('CLONE','is_score')

        # REMOVE：删除中间文件
        self.is_remove = config.getboolean('REMOVE','is_remove')

        # MULT: 多文件评估
        self.sole_or_mult = config.getint('MULT','sole_or_mult')
        self.mult_path = re.split(r'[;,\s]\s*',config.get('MULT','mult_path'))
        temp_mult_mode = re.split(r'[;,\s]\s*',config.get('MULT','mult_mode'))
        self.mult_mode = [int(i) for i in temp_mult_mode]
        temp_mult_is_sort = re.split(r'[;,\s]\s*', config.get('MULT', 'mult_is_sort'))
        m_i_s = []
        for i in temp_mult_is_sort:
            if i == 'False':
                m_i_s.append(False)
            elif i == 'True':
                m_i_s.append(True)
        self.mult_is_sort = m_i_s
        temp_mult_is_score = re.split(r'[;,\s]\s*', config.get('MULT', 'mult_is_score'))
        m_i_score = []
        for i in temp_mult_is_score:
            if i == 'False':
                m_i_score.append(False)
            elif i == 'True':
                m_i_score.append(True)
        self.mult_is_score = m_i_score
        temp_mult_is_intersect = re.split(r'[;,\s]\s*', config.get('MULT', 'mult_is_intersect'))
        m_i_i = []
        for i in temp_mult_is_intersect:
            if i == 'False':
                m_i_i.append(False)
            elif i == 'True':
                m_i_i.append(True)
        self.mult_is_intersect = m_i_i
        temp_mult_is_diff = re.split(r'[;,\s]\s*', config.get('MULT', 'mult_is_diff'))
        m_i_diff = []
        for i in temp_mult_is_diff:
            if i == 'False':
                m_i_diff.append(False)
            elif i == 'True':
                m_i_diff.append(True)
        self.mult_is_diff = m_i_diff
        temp_mult_minTokens1 = [int(i) for i in re.split(r'[;,\s]\s*', config.get('MULT', 'mult_minTokens'))]
        temp_mult_minTokens2 = []
        for i in temp_mult_minTokens1:
            temp_mult_minTokens3 = []
            temp_mult_minTokens3.append(i)
            temp_mult_minTokens2.append(temp_mult_minTokens3)
        self.mult_minTokens = temp_mult_minTokens2
        self.mult_score_path = config.get('MULT','mult_score_path')
