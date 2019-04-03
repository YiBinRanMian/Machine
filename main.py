import os
import re
from sample import readinput
from sample import stuTest
from sample import readoutput
from pyAstPrint import pyAst
from genClone import genclone
from diff import diffComp
from codeStyle import valOutput
from codeStyle import genOutStr
from config import configReader
from threading import Timer
import openpyxl

def time_limit(interval):
    def wraps(func):
        def time_out():
            raise RuntimeError()
        def deco(*args, **kwargs):
            timer = Timer(interval, time_out)
            timer.start()
            res = func(*args, **kwargs)
            timer.cancel()
            return res
        return deco
    return wraps

def floatcomparelist(list1,list2,is_intersect):
    intersectlist = [i for i in list1 if i in list2]
    if len(list1) != len(list2):
        if is_intersect:
            if float(len(intersectlist)/len(list2)) > 1:
                return 2 - float(len(intersectlist)/len(list2))
            else:
                return float(len(intersectlist)/len(list2))
        else:
            return 0
    else:
        for i in range(len(list1)):
            if float(list1[i]) != float(list2[i]):
                if is_intersect:
                    if float(len(intersectlist) / len(list2)) > 1:
                        return 2 - float(len(intersectlist) / len(list2))
                    else:
                        return float(len(intersectlist)/len(list2))
                else:
                    return 0
        return 1

def intcomparelist(list1,list2,is_intersect):
    list1 = [int(float(i)) for i in list1]
    list2 = [int(float(i)) for i in list2]
    intersectlist = [i for i in list1 if i in list2]
    if len(list1) != len(list2):
        if is_intersect:
            if float(len(intersectlist)/len(list2)) > 1:
                return 2 - float(len(intersectlist)/len(list2))
            else:
                return float(len(intersectlist)/len(list2))
        else:
            return 0
    else:
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                if is_intersect:
                    if float(len(intersectlist) / len(list2)) > 1:
                        return 2 - float(len(intersectlist) / len(list2))
                    else:
                        return float(len(intersectlist)/len(list2))
                else:
                    return 0
        return 1

def strcomparelist(list1,list2,is_intersect):
    intersectlist = [i for i in list1 if i in list2]
    if len(list1) != len(list2):
        if is_intersect:
            return float(len(intersectlist)/len(list2))
        else:
            return 0
    else:
        for i in range(len(list1)):
            if str(list1[i]) != str(list2[i]):
                if is_intersect:
                    return float(len(intersectlist)/len(list2))
                else:
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
                f.close()
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
    for i in range(num):
        for j in clonedict[i]:
            if j.split()[0] == fname:
                clonedict1[num1] = clonedict[i].copy()
                num1+=1
                break
    return clonedict1

@time_limit(60)
def scoring(path,mode,clist,clist2,minTokens,stride,similarity,distance,res_rate,none_clone_rate,style_rate,is_sort=True,is_score = True, is_intersect = False,is_diff = False):
    print("""
----------------------------------------------------------------------------------------------------
begin scoring ...
    """)
    scorename = path+'/grading/scores'
    scorefile = open(scorename,'w')
    inlist = readinput(path+'/grading/input')
    outlist = readoutput(path+'/grading/output')
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1]=='.py' and filename != 'temp.py':
            print('filename: '+ filename)
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
                        score += intcomparelist(numlist,anslist,is_intersect)
                    elif mode == 1:
                        numlist = re.findall('\d+\.?\d*', outstr)
                        if is_sort:
                            numlist.sort(key=lambda d: float(d))
                        score += floatcomparelist(numlist, anslist,is_intersect) * 0.8
                    elif mode == 2:
                        list1 = re.split(r'[;,\s]\s*', outstr)
                        list2 = re.split(r'[;,\s]\s*',outlist[i])
                        score += strcomparelist(list1,list2,is_intersect)
            noneClone = 1
            res = score/paramLen
            if is_diff:
                if filename.rstrip('.py') in clist and filename in clist2:
                    noneClone = 0
            else:
                if filename.rstrip('.py') in clist:
                    noneClone = 0
            valout = valOutput(path,filename)
            if is_score:
                pg_score += 'score = ' + str(float('%.2f' % res)) + ' * '+ str(res_rate) +' + ' + str(noneClone) + ' * '+ str(none_clone_rate) +' + ' + str(
                    float('%.2f' % valout)) + ' * '+str(style_rate)+''
                res = res * res_rate + noneClone * none_clone_rate + valout * style_rate

            else:
                pg_score += 'score = ' + str(float('%.2f' % res)) + ' * ' + str(res_rate) + ' + ' + str(
                    float('%.2f' % valout)) + ' * ' + str((1-res_rate)) + ''
                res = res * res_rate + valout * (1 - res_rate)

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
            if res < 0.7:
                inspect_file1 = open(path + '/' + filename,'r')
                inspect_file2 = open(path + '/inspection/' + filename,'w')
                inspect_file3 = open(path + '/inspection/' + filename.rstrip('.py') + '.txt','w')
                inspect_file2.writelines(inspect_file1.readlines())
                inspect_file3.write(outputstr)
                inspect_file1.close()
                inspect_file2.close()
                inspect_file3.close()
            outputfile.write(outputstr)
            outputfile.close()
            print(filename+' ' + str(float('%.2f'%res)) +' finished.\n' + 'see detains in'+path+'/log/'+ filename+'\n')


def renamefiles(path):
    if not os.path.exists(path + '/logs'):
        os.mkdir(path + '/logs')
    if not os.path.exists(path + '/inspection'):
        os.mkdir(path+ '/inspection')
        os.mkdir(path + '/inspection/grading')
        input1 = open(path + '/grading/input','r')
        input = open(path + '/inspection/grading/input','w')
        input.writelines(input1.readlines())
        output1 = open(path + '/grading/output','r')
        output = open(path + '/inspection/grading/output','w')
        output.writelines(output1.readlines())
        input.write('')
        output.write('')
        output1.close()
        input1.close()
        input.close()
        output.close()
    for filename in os.listdir(path) :
        if os.path.splitext(filename)[1] == 'py'  and filename != 'temp.py':
            newname = filename.replace(' ','')
            os.rename(os.path.join(path+'/'+filename),os.path.join(path+'/'+newname))

def removeTempFiles(path):
    os.remove(os.path.join(path + 'temp.py'))
    for file in os.listdir(path + 'times'):
        os.remove(os.path.join(path + 'times/' + file))
    os.removedirs(os.path.join(path + 'times'))
    for file in os.listdir(path + 'vectors'):
        os.remove(os.path.join(path + 'vectors/' + file))
    os.removedirs(os.path.join(path + 'vectors'))
    for file in os.listdir(path.rstrip('/')):
        if os.path.splitext(file)[1] == '.txt':
            os.remove(os.path.join(path + file))

def main():
    configer = configReader()
    print('\n'.join(['%s:%s' % item for item in configer.__dict__.items()]))
    mode = configer.mode
    mult_mode = configer.mult_mode
    minTokens = configer.minTokens
    stride = configer.stride
    similarity = configer.similarity
    distance = configer.distance
    is_score = configer.is_score
    is_sort = configer.is_sort
    mult_is_sort = configer.mult_is_sort
    mult_is_score = configer.mult_is_score
    mult_minTokens = configer.mult_minTokens
    mult_is_intersect = configer.mult_is_intersect
    mult_is_diff = configer.mult_is_diff
    sole_or_mult = configer.sole_or_mult
    path = configer.path
    mult_path = configer.mult_path
    is_remove = configer.is_remove
    res_rate = configer.res_rate
    none_clone_rate = configer.none_clone_rate
    is_diff = configer.is_diff
    style_rate = configer.style_rate
    is_intersect = configer.is_intersect
    diff = configer.diff
    mult_score_path = configer.mult_score_path
    if sole_or_mult == 0:
        renamefiles(path)
        pyAst(path)
        genclone(path, minTokens, stride, similarity, distance)
        clist = getCloneFile(path, minTokens, stride, similarity, distance)
        print(clist)
        clist2 = diffComp(path, diff)
        scoring(path, mode, clist, clist2, minTokens, stride, similarity, distance, res_rate, none_clone_rate,
                style_rate, is_sort, is_score, is_intersect,is_diff)
        if is_remove:
            removeTempFiles(path + '/')
    elif sole_or_mult == 1:
        mult_index = 0
        for path in mult_path:
            renamefiles(path)
            pyAst(path)
            genclone(path, mult_minTokens[mult_index], stride, similarity, distance)
            clist = getCloneFile(path, mult_minTokens[mult_index], stride, similarity, distance)
            clist2 = diffComp(path, diff)
            scoring(path, mult_mode[mult_index], clist, clist2, mult_minTokens[mult_index], stride, similarity, distance, res_rate,
                    none_clone_rate,
                    style_rate, mult_is_sort[mult_index], mult_is_score[mult_index], mult_is_intersect[mult_index],mult_is_diff[mult_index])
            if is_remove:
                removeTempFiles(path + '/')
            mult_index += 1
        record_2_txt_and_xlsx(mult_score_path,mult_path)
    elif sole_or_mult == 2:
        record_2_txt_and_xlsx(mult_score_path,mult_path)

def record_2_txt_and_xlsx(mult_score_path,mult_path):
    w = openpyxl.Workbook()
    sheet = w.active
    sheet.title = 'score_records'
    recode_file = mult_score_path + '/scores'
    mult_score = open(recode_file, 'w')
    score_dict = {}
    fn = re.compile(r'(.*\.py)\s(\d+\.?\d*)')
    for path in mult_path:
        grade_path = path + '/grading/scores'
        source = open(grade_path, 'r')
        score_recodes = source.readlines()
        for line in score_recodes:
            score_recode = re.match(fn, line.rstrip('\n'))
            fname = score_recode.group(1)[:9]
            score = score_recode.group(2)
            if not score_dict.__contains__(fname):
                score_dict[fname] = float(score)
            else:
                score_dict[fname] += float(score)
        source.close()
    score_table = []
    for fname in score_dict:
        score_line = []
        score_dict[fname] = score_dict[fname] / len(mult_path)
        score_line.append(fname)
        score_line.append(str(int(float('%.2f' % score_dict[fname]) * 100)))
        mult_score.write(fname + ' ' + str(float('%.2f' % score_dict[fname])) + '\n')
        score_table.append(score_line)
    for i in range(len(score_table)):
        for j in range(len(score_table[i])):
            sheet.cell(row=i + 1, column=j + 1, value=str(score_table[i][j]))
    w.save(mult_score_path + '/score_records.xlsx')
    mult_score.close()

if __name__ == "__main__":
    main()
