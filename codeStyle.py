import sys
import os
import re

operValue = ['&','/','>','<','%','*','-','=','+']
doubleOperValue = ['==','>=','<=','+=','//','!=']
def valLine(path,fname):
    path = path +'/'+fname
    linelist = open(path,'r').readlines()
    lineCount = [len(line) for line in linelist if len(line) > 80]
    if len(lineCount)>0: return 0
    else :return 1

def valSemi(path,fname):
    path = path +'/'+fname
    linelist = open(path,'r').readlines()
    ms1 = re.compile('.*;.*')
    ms2 = re.compile('.*(.*".*;.*".*).*')
    st = ''
    for line in linelist:
        st += line
    semi = re.findall(ms1,st)
    semi2 = re.findall(ms2,st)
    if len(semi) - len(semi2)>0: return 0
    else :return 1

def valBackslash(path,fname):
    path = path + '/' + fname
    linelist = open(path, 'r').readlines()
    ms1 = re.compile(r'.*\\\n.*')
    st = ''
    for line in linelist:
        st += line
    semi = re.findall(ms1, st)
    if len(semi) > 0: return 0
    else: return 1

def getLino(path,lino):
    path = path.rstrip('.py')+'.txt'
    rAst = []
    for line in open(path,'r').readlines():
        line = line.split()
        if len(line) > 3 and line[3] == str(lino):
            rAst.append(line[2])
    return rAst

def valTuple(path,fname):
    path = path + '/' + fname
    linelist = open(path,'r').readlines()
    ms1 = re.compile(r'if.*\(.*\).*:')
    for i in range(len(linelist)):
        if re.search(ms1,linelist[i]):
            terminalList = getLino(path,i+1)
            if 'Tuple' not in terminalList:
                return 0
    return 1

def valTab(path,fname):
    path = path + '/' + fname
    linelist = open(path,'r').readlines()
    ms1 =  re.compile('.*\t.*')
    for line in linelist:
        if re.match(ms1,line):
            return 0
    return 1

def valSpace1(path,fname):
    path = path + '/' + fname
    linelist = open(path,'r').readlines()
    ms1 = re.compile(r'.*\(\s.*|.*\s\).*|.*\[\s.*|.*\s\].*|.*{\s.*|.*\s}.*|.*\s,.*|.*\s;.*|.*\s:.*')
    note1 = re.compile('#[^\r\n]*')
    note2 = re.compile('.*(""".*?""")')
    for line in linelist:
        if re.search(note1,line) or re.search(note2,line):
            continue
        if re.match(ms1,line):
            return 0
    return 1

def valSpace2(path,fname):
    path = path + '/' + fname
    linelist = open(path,'r').readlines()
    note1 = re.compile('#[^\r\n]*')
    note2 = re.compile('.*(""".*?""")')
    for line in linelist:
        if re.search(note1,line) or re.search(note2,line):
            continue
        for oper in operValue:
            if line.find(oper) != -1:
                if not re.search('(?<=\s)'+oper+'(?=\s)',line):
                    flag = 0
                    for doper in doubleOperValue:
                        if line.find(doper) != -1:
                            flag = 1
                            if doper[0] == '+':
                                doper = '\+='
                            if re.search('(?<!\s)'+ doper + '(?=\s)|(?<=\s)' + doper + '(?!\s)|(?<!\s)' + doper + '(?!\s)', line):
                                return 0
                    if flag == 0:
                        return 0
    return 1

def valImport(path,fname):
    path = path + '/' + fname
    linelist = open(path, 'r').readlines()
    ms1 = re.compile(r'.*import.*,.*\n')
    for line in linelist:
        if re.match(ms1,line):
            return 0
    return 1

def valStmt(path,fname):
    path = path + '/' + fname
    linelist = open(path, 'r').readlines()
    ms1 = re.compile('else:|try:|except\sValueError:')
    ms2 = re.compile('else:\s*\n|except\sValueError:\s*\n|try:\s*\n')
    for line in linelist:
        if re.search(ms1,line):
            if not re.search(ms2,line):
                return 0
    return 1

def valName(path, fname):
    path1 = path + '/' + fname
    path2 = path1.rstrip('.py')+'.txt'
    linelist = open(path2,'r').readlines()
    for line in linelist:
        line = line.split()
        if len(line)>=5:
            if line[2] == 'Name' or line[2] == 'arg':
                if not line[4].strip('\'').islower():
                    return 0
            elif line[2] == 'ClassDef':
                if line[4].strip('\'').isupper() or line[4].strip('\'').islower():
                    return 0
            elif line[2] == 'FunctionDef':
                if not line[4].strip('\'').islower():
                    return 0
    if not fname.islower():
        return 0
    return 1

def outputGrade(path,fname):
    grade = [0 for i in range(10)]
    grade = [valLine(path,fname),valSemi(path,fname),valBackslash(path,fname),valTuple(path,fname),valTab(path,fname),valSpace1(path,fname),valSpace2(path,fname),valImport(path,fname),valStmt(path,fname),valName(path,fname)]
    return grade

def valOutput(path,fname):
    grade = outputGrade(path,fname)
    score = 0
    for i in grade:
        score += i
    score = score/10
    return float('%.1f'%score)

def genOutStr(path,fname):
    grade = outputGrade(path,fname)
    outstr = ['每行不超过80个字符\n','不要在行尾加分号, 也不要用分号将两条命令放在同一行\n','不要使用反斜杠连接行\n',
              '除非是用于实现行连接, 否则不要在返回语句或条件语句中使用括号\n','用4个空格来缩进代码,不要使用Tab\n',
              '括号内不要有空格 不要在逗号, 分号, 冒号前面加空格\n',' 在二元操作符两边都要加上一个空格\n',
              '每个导入应该独占一行\n','通常每个语句应该独占一行 如果是if语句, 只有在没有else时才能这样做,特别地, 绝不要对 try/except 这样做\n',
              '变量全小写 文件名全小写 类名大小写混合 方法名全小写\n']
    outputstr = '---------------代码风格建议---------------\n'
    for i in range(len(grade)):
        if grade[i] == 0:
            outputstr += outstr[i]
    return outputstr


