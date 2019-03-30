def readinput(fname):
    fin = open(fname,'r')
    inlist = []
    tempstr = ''
    firstline = True
    line = fin.readline()
    while line:
        tempstr+=line

        line = fin.readline()
        if line == '\n':
            if firstline:
                inlist.append(tempstr)
                firstline = False
            else:
                inlist.append(tempstr[1:])
            tempstr = ''

    if tempstr!='':
        if firstline:
            inlist.append(tempstr)
            firstline = False
        else:
            inlist.append(tempstr[1:])
    fin.close()
    return inlist

def readoutput(fname):
    fout = open(fname,'r')
    outlist = []
    tempstr = ''
    firstline = True
    line = fout.readline()
    while line:
        tempstr+=line

        line = fout.readline()
        if line == '\n':
            if firstline:
                outlist.append(tempstr)
                firstline = False
            else:
                outlist.append(tempstr[1:])
            tempstr = ''

    if tempstr!='':
        if firstline:
            outlist.append(tempstr)
            firstline = False
        else:
            outlist.append(tempstr[1:])
    fout.close()
    return outlist


def list2str(l):
    s = ''
    for i in range(len(l)):
        s+=l[i]
    return s

def stuTest(fname,i,path):
    f = open(fname, 'r')
    if i != -1:
        preString ="""
import sys,os,sample
savein = sys.stdin
inlist = sample.readinput('"""+path+"""/grading/input')
tempfile = open('"""+path+"""/grading/tempfile', 'w')
tempfile.write(inlist["""+str(i)+"""])
tempfile.close()
tempfile = open('"""+path+"""/grading/tempfile', 'r')
sys.stdin = tempfile
"""
        s = list2str(f.readlines())
        preString += s
        endString = """
sys.stdin = savein
os.remove(os.path.join('"""+path+"""/grading/tempfile'))
        """
        preString += endString
    else:
        preString = list2str(f.readlines())
    pref = open(path+'/temp.py', 'w')
    pref.write(preString)
    pref.close()