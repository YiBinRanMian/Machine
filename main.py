import os
import re
import sys
from sample import readinput
from sample import stuTest
from sample import readoutput
from pyAstPrint import pyAst
from genClone import genclone
from diff import diffComp
from codeStyle import valOutput
from codeStyle import genOutStr
from config import configReader

def floatcomparelist(list1,list2):
    if len(list1) != len(list2):
        return 0
    else:
        print(list1)
        print(list2)
        for i in range(len(list1)):
            if float(list1[i]) != float(list2[i]):
                return 0
        return 1

def intcomparelist(list1,list2):
    list1 = [int(float(i)) for i in list1]
    list2 = [int(float(i)) for i in list2]
    intersectlist = [i for i in list1 if i in list2]

    if len(list1) != len(list2):
        return float(len(intersectlist)/len(list2))
    else:
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return float(len(intersectlist)/len(list2))
        return 1

def strcomparelist(list1,list2):
    if len(list1) != len(list2): return 0
    else:
        for i in range(len(list1)):
            if str(list1[i]) != str(list2[i]):
                return 0
        return 1

def getAnsList(mode,answer,is_sort=True):
    anslist = []
    if mode == 0:
        anslist = re.findall('\d+',answer)
        if is_sort:
            anslist.sort(key=lambda d: int(d))
    elif mode == 1:
        anslist = re.findall('\d+\.?\d*',answer)
        if is_sort:
            anslist.sort(key=lambda d:float(d))
    return anslist

def getCloneFile(path,minT,strI,simI,disT):
    clist = []
    cl = re.compile('.*FILE (.*) LINE.*')
    sl = re.compile('.*'+path+'/(.*)\.txt.*')
    cluster_path = path + '/clusters'
    for i in range(len(minT)):
        for j in range(len(strI)):
            for k in range(len(simI)):
                filename = cluster_path + '/post_cluster_vdb_'+str(minT[i])+'_'+str(strI[j])+'_allg_'+str(simI[k])+'_50'
                f = open(filename,'r')
                source = f.readlines()
                for line in source:
                    if cl.match(line):
                        if(sl.match(cl.match(line).group(1))):
                            fn = sl.match(cl.match(line).group(1))
                            if fn.group(1) not in clist:
                                clist.append(fn.group(1))
    return clist

def getClonePairs(path,minT,strI,simI,disT,fname):
    cluster_path = path + '/clusters'
    cl = re.compile('.*FILE (.*) (LINE:.*)\sNODE_KIND.*')
    sl = re.compile('.*'+path+'/(.*)\.txt.*')
    num = 0
    clonedict = {}
    clonedict1 = {}
    for i in range(len(minT)):
        for j in range(len(strI)):
            for k in range(len(simI)):
                filename = cluster_path + '/post_cluster_vdb_'+str(minT[i])+'_'+str(strI[j])+'_allg_'+str(simI[k])+'_50'
                source = open(filename,'r').readlines()
                clonelist = []
                for line in source:
                    if line != '\n':
                        st1 = sl.match(cl.match(line).group(1)).group(1) +'.py '+ cl.match(line).group(2)
                        clonelist.append(st1)
                    else:
                        clonedict[num] = clonelist.copy()
                        num += 1
                        clonelist.clear()
    num1 = 0
    for i in range(num-1):
        for j in clonedict[i]:
            if j.split()[0] == fname:
                clonedict1[num1] = clonedict[i].copy()
                num1+=1
                break

    return clonedict1


def scoring(path,mode,clist,clist2,minTokens,stride,similarity,distance,is_sort=True):
    scorename = path+'/grading/scores'
    scorefile = open(scorename,'w')
    inlist = readinput(path+'/grading/input')
    outlist = readoutput(path+'/grading/output')
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1]=='.py' and filename != 'temp.py':
            outputfile = open(path + '/logs/' + filename.rstrip('.py') + '.txt','w')
            pg_input = 'Input:\n\n'
            pg_output = '----------------------------------------\nOutput of '+filename+':\n\n'
            pg_score = '----------------------------------------\nscore of ' + filename+':\n\n'
            score = 0
            paramLen = len(outlist)
            for i in range(paramLen):
                anslist = getAnsList(mode,outlist[i],False)
                if inlist == []:
                    i = -1
                else:
                    pg_input += inlist[i]
                stuTest(path+'/'+filename,i,path)
                outcome = os.popen('python3 '+path+'/temp.py')
                outstr = outcome.read()
                pg_output +=outstr +'\n'
                if outstr == outlist[i]:
                    score +=1
                else:
                    if mode == 0:
                        numlist = re.findall('\d+\.?\d*',outstr)
                        if is_sort:
                            numlist.sort(key=lambda d:float(d))
                        score += intcomparelist(numlist,anslist)
                        # if intcomparelist(numlist,anslist):
                        #     score += 1
                        # else:
                        #     score += 0
                    elif mode == 1:
                        numlist = re.findall('\d+\.?\d*', outstr)
                        if is_sort:
                            numlist.sort(key=lambda d: float(d))
                        if floatcomparelist(numlist, anslist):
                            score += 0.8
                        else:
                            score += 0
                    elif mode == 2:
                        score += 0
            noneClone = 1
            res = score/paramLen
            if filename[0:9] in clist and filename in clist2:
                noneClone = 0
            valout = valOutput(path,filename)
            pg_score += 'score = ' + str(float('%.2f'%res)) + ' * 0.6 + ' + str(noneClone) + ' * 0.2 + ' + str(float('%.2f'%valout)) + ' * 0.2'
            res = res *0.6 + noneClone * 0.2 + valout *0.2
            pg_score += ' = '+str(float('%.2f'%res)) + '\n\n'
            scorefile.write(filename+" "+str(float('%.2f'%res))+"\n")
            clone_report = getClonePairs(path,minTokens,stride,similarity,distance,filename)
            clone_str = '----------------------------------------\nClone report of '+filename+':\n\n'
            if clone_report == {}:
                clone_str+= 'None\n'
            else:
                for cindex in range(len(clone_report)):
                    for fstr in clone_report[cindex]:
                        clone_str+=fstr+'\n'
                    clone_str+='\n'

            outputstr = pg_input + pg_output + pg_score + clone_str + genOutStr(path,filename)
            outputfile.write(outputstr)

def renamefiles(path):
    if not os.path.exists(path + '/logs'):
        os.mkdir(path + '/logs')
    for filename in os.listdir(path) :
        if os.path.splitext(filename)[1] == 'py'  and filename != 'temp.py':
            newname = filename.replace(' ','')
            os.rename(os.path.join(path+'/'+filename),os.path.join(path+'/'+newname))

def removeTempFiles(path):
    os.remove(os.path.join(path + 'temp.py'))
    # for file in os.listdir(path + 'clusters'):
    #     os.remove(os.path.join(path + 'clusters/' + file))
    # os.removedirs(os.path.join(path + 'clusters'))
    for file in os.listdir(path + 'times'):
        os.remove(os.path.join(path + 'times/' + file))
    os.removedirs(os.path.join(path + 'times'))
    for file in os.listdir(path + 'vectors'):
        os.remove(os.path.join(path + 'vectors/' + file))
    os.removedirs(os.path.join(path + 'vectors'))
    for file in os.listdir(path.rstrip('/')):
        if os.path.splitext(file)[1] == '.txt':
            os.remove(os.path.join(path + file))




if __name__ == "__main__":
    configer = configReader()
    mode = configer.mode
    minTokens = configer.minTokens
    stride = configer.stride
    similarity = configer.similarity
    distance = configer.distance
    is_sort = configer.is_sort
    path = configer.path
    renamefiles(path)
    pyAst(path)
    genclone(path,minTokens,stride,similarity,distance)
    clist = getCloneFile(path,minTokens,stride,similarity,distance)
    clist2 = diffComp(path,0.83)
    scoring(path,mode,clist,clist2,minTokens,stride,similarity,distance,is_sort)
    removeTempFiles(path + '/')
