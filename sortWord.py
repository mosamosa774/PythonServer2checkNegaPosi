# coding: UTF-8
import MeCab as mec
import sys
import re

def addWord(word,_list = []):
    exist = False
    if(not len(_list) == 0):
        for i in range(len(_list)):
            if(_list[i][0] == word):
                exist = True
                _list[i] = (word,_list[i][1]+1)

    if(not exist):
        _list.append( (word,1) )
    return _list

def printMax(_list,num):
    tmp = [0]*num
    maxs = [-1]*num
    for i in _list:
        for j in range(len(maxs)):
            if(i[1] > maxs[j]):
                tmp[j] = i
                maxs[j] = i[1]
                break
    for i in tmp:
        print(i)

m = mec.Tagger ("-Ochasen")

verb = []
noun = []

with open(sys.argv[1],encoding="utf-8") as f:
    s = f.read()
    s =  s.split('。')
    for _s in s:
        res = m.parse(_s)
        lines = res.split('\n')
        items = (re.split('[\t,]', line) for line in lines)
        for item in items:
            try:
                if(re.search('動詞',item[3])):
                    verb = addWord(item[2],verb)
                elif(re.search('名詞',item[3])):
                    noun = addWord(item[2],noun)
            except:
                pass

print('verb appeared ranking best 3!!!')
printMax(verb,10)
print('noun appeared ranking best 3!!!')
printMax(noun,10)