# coding: UTF-8
import MeCab as mec
import sys
import re

noun = {}
verb = {}


def init():
    noun = {}
    verb = {}
    with open('pn.csv.m3.120408.trim', encoding="utf-8") as f:
        texts = f.read().split('\n')
        for txt in texts:
            word = txt.split('\t')
            if(word[0][0] in noun):
                noun[word[0][0]].append(word)
            else:
                noun[word[0][0]] = [word]
    # p: positive, n: negative, a: negativeっぽい, e: neutral
    with open('wago.121808.pn', encoding="utf-8") as f:
        texts = f.read().split('\n')
        for txt in texts:
            word = txt.split('\t')
            if(word[1][0] in verb):
                verb[word[1][0]].append(word)
            else:
                verb[word[1][0]] = [word]
        return noun, verb


def analyze(noun, verb, contents, everyLine, limit):
    m = mec.Tagger("-Ochasen")
    texts = re.split('[。\n！？!?　()（）]', contents)
    sum_n_p = 0
    body = ""
    for txt in texts:
        n_p = 0
        res = m.parse(txt)
        lines = res.split('\n')
        items = (re.split('[\t,]', line) for line in lines)
        for item in items:
            try:
                if(re.search('動詞', item[3])):
                    for i in verb.get(item[2][0]):
                        # print(i[1],item[2])
                        if(i[1] == item[2]):
                            if(re.search('ポジ', i[0])):
                                n_p += 1
                            elif(re.search('ネガ', i[0])):
                                n_p -= 1
                else:
                    for i in noun.get(item[2][0]):
                        # print(i[0],item[2])
                        if(i[0] == item[2]):
                            if(i[1] == 'p'):
                                n_p += 1
                            elif(i[1] == 'n'):
                                n_p -= 1
                            elif(i[1] == 'a'):
                                n_p -= 1
                if (re.match('ない|無い', item[2])):
                    n_p = - n_p
            except:
                pass
        if(not txt == "" and everyLine > 0):
            if(everyLine == 1 and abs(n_p) >= int(limit)):
                body += txt+','+str(n_p)+'\n'
            elif(everyLine > 1):
                body += txt+','+str(n_p)+'\n'
        else:
            sum_n_p += n_p
    if(everyLine == 0):
        return str(sum_n_p)
    else:
        return body


#noun, verb = init()
#print(analyze(noun, verb, sys.argv[1], int(sys.argv[2]), int(sys.argv[3])))
