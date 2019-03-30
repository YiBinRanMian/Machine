import difflib
import sys
import os
import re

def stripNotes(fname,path):
    note1 = re.compile('#[^\r\n]*')
    note2 = re.compile('.*(""".*?""")')
    f1 = path + '/' + fname
    t1 = open(f1, 'r')
    s1 = t1.readlines()
    st1 = ''
    for i in range(len(s1)):
        st1 += s1[i]
    m = re.findall(note1, st1)
    for i in range(len(s1)):
        if re.match(note1, s1[i]):
            s1[i] = ''
    st2 = ''
    for i in range(len(s1)):
        st2 += s1[i].strip()
    m2 = re.findall(note2, st2)
    for i in range(len(m2)):
        st2 = st2.replace(m2[i], '')
    return st2

def diffComp(path,ratio):
    clist = []
    filelist = [filename for filename in os.listdir(path) if os.path.splitext(filename)[1] == '.py' and filename != 'temp.py']
    for i in range(len(filelist)-1):
        for j in range(i+1,len(filelist)):
            st1 = stripNotes(filelist[i],path)
            st2 = stripNotes(filelist[j],path)
            diffRatio = difflib.SequenceMatcher(None,st1,st2).quick_ratio()
            if diffRatio >=ratio:
                if filelist[i] not in clist:
                    clist.append(filelist[i])
                if filelist[j] not in clist:
                    clist.append(filelist[j])
    return clist