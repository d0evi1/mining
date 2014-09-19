#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------
# @file     simhash_filter.py
#
# @brief    use simhash to filter the dup files.
# @date     2014.9.18
#-----------------------------------------

import sys
import jieba
import smhasher
import jieba.analyse
import jieba.posseg
import re

key_map = {}
simhash_map = {}
simhash_index_map1 = {}
simhash_index_map2 = {}
simhash_index_map3 = {}
simhash_index_map4 = {}
simhash_index_map5 = {}



class SimhashFilter:
    cnt_list = []

    def __init__(self):
        self.cnt_list = [0 for i in range(8)] 

    def clear_cnt(self):
        self.cnt_list = [0 for i in range(8)]

    def init_context(self):
        jieba.initialize()
        jieba.enable_parallel(4)
        #jieba.load_userdict(MYDICT)

    def get_hash64(self, str):
        return smhasher.murmur3_x86_64(str)

    def get_simhash(self, text):
        self.clear_cnt()
        seg_list = jieba.posseg.cut(text)

        hist = [0 for i in range(64)]

        word_list = []
        for word in list(seg_list):
            if word.flag == 'x' or word.flag == 'm':
                continue
            elif word.flag == '' or word.flag[0] == 'u':
                continue
            elif word.flag == 'eng':
                continue

            if word.word not in set(word_list):
                word_list.append(word.word)
            else:
                continue

            seg = word.word
            str = seg.encode('utf8')

            hash = self.get_hash64(str)
            for i in range(0, 64):
                val = (-1 if (hash & (1<<i) == 0) else 1)
                hist[i] += val


        simHash = 0
        for i in range(0, 64):
            t = (1 if (hist[i]>=0) else 0)
            t <<= i
            simHash |= t

        return simHash

    def haming_distance(self, simhash1, simhash2):
        xor_val = simhash1 ^ simhash2
        i = 0
        while xor_val > 0:
            xor_val &= (xor_val - 1)
            i+=1

        return i

    def check_simhash(self, simhash):
        index1 = ((simhash & 0xfff0000000000000) >> 52)
        index2 = ((simhash & 0x000fff0000000000) >> 40)
        index3 = ((simhash & 0x000000fff0000000) >> 28)
        index4 = ((simhash & 0x000000000fff0000) >> 16)
        index5 = (simhash & 0x000000000000ffff) 

        if simhash_index_map1.has_key(index1):
            hash_list = simhash_index_map1[index1]
            for h in hash_list:
                dist = self.haming_distance(simhash, h)
                if dist == 0:
                    return 0
                elif dist < 5:
                    return dist

        if simhash_index_map2.has_key(index2):
            hash_list = simhash_index_map2[index2]
            for h in hash_list:
                dist = self.haming_distance(simhash, h)
                if dist == 0:
                    return 0
                elif dist < 5:
                    return dist
        
        if simhash_index_map3.has_key(index3):
            hash_list = simhash_index_map3[index3]
            for h in hash_list:
                dist = self.haming_distance(simhash, h)
                if dist == 0:
                    return 0
                elif dist < 5:
                    return dist

        if simhash_index_map4.has_key(index4):
            hash_list = simhash_index_map4[index4]
            for h in hash_list:
                dist = self.haming_distance(simhash, h)
                if dist == 0:
                    return 0
                elif dist < 5:
                    return dist

        if simhash_index_map5.has_key(index5):
            hash_list = simhash_index_map5[index5]
            for h in hash_list:
                dist = self.haming_distance(simhash, h)
                if dist == 0:
                    return 0
                elif dist < 5:
                    return dist

        return -1

    # 12/ 12/ 12/ 12/ 16
    def add_one_hash(self, simhash):
        if simhash_map.has_key(simhash):
            return 0
        else:
            simhash_map[simhash] = simhash
            index1 = ((simhash & 0xfff0000000000000) >> 52)
            index2 = ((simhash & 0x000fff0000000000) >> 40)
            index3 = ((simhash & 0x000000fff0000000) >> 28)
            index4 = ((simhash & 0x000000000fff0000) >> 16)
            index5 = (simhash & 0x000000000000ffff)

            if simhash_index_map1.has_key(index1):
                simhash_index_map1[index1].append(simhash)
            else:
                simhash_index_map1[index1] = [simhash]

            if simhash_index_map2.has_key(index2):
                simhash_index_map2[index2].append(simhash)
            else:
                simhash_index_map2[index2] = [simhash]

            if simhash_index_map3.has_key(index3):
                simhash_index_map3[index3].append(simhash)
            else:
                simhash_index_map3[index3] = [simhash]

            if simhash_index_map4.has_key(index4):
                simhash_index_map4[index4].append(simhash)
            else:
                simhash_index_map4[index4] = [simhash]

            if simhash_index_map5.has_key(index5):
                simhash_index_map5[index5].append(simhash)
            else:
                simhash_index_map5[index5] = [simhash]

            return 1


    def is_exists(self, simhash):
        ret = self.check_simhash(simhash)

        if ret > 0:
            self.add_one_hash(simhash)
            return 1
        elif ret == 0:
            return 1
        else:
            self.add_one_hash(simhash)
            return 0

def stringutil_isalpha(c):
    if (c >= 'a' and c <= 'z') or ( c >= 'A' and c <= 'Z'):
        return 1
    else:
        return 0

def stringutil_isnum(c):
    if c >= '0' and c <= '9':
        return 1
    else:
        return 0


def stringutil_isotherchar(c):
    if c == '_' or c == '-' or c == '*':
        return 1
    else:
        return 0

def stringutil_islegalusername(c):
    if(stringutil_isalpha(c) > 0
            or stringutil_isnum(c) > 0
            or stringutil_isotherchar(c) > 0):
        return 1
    else:
        return 0

def stringutil_isdoubledigit(lo, hi):
    if lo == 0xa3 and ((hi >= 0xb0 and hi <= 0xb9) or hi == 0xae):
        return 1
    else:
        return 0

def filter_username(input):
    output = ""
    iCur = 0
    iEnd = len(input)
    while iCur < iEnd:
        while iCur < iEnd and input[iCur] != '@':
            if input[iCur] == '|':
                iCur += 1
            else:
                output += input[iCur]
                iCur += 1

        if iCur < iEnd:
            iCur += 1
            tmp_str = input[iCur:]
            j = 0
            for i in range(0, len(tmp_str)):
                if stringutil_islegalusername(tmp_str[i]) == 0:
                    break
                j+=1

            iCur += j

        return output


def filter_topic(input):
    isCheck = 0
    output = ""
    half_topic = ""
    for i in xrange(0, len(input)):
        if input[i] == '#' and isCheck == 0:
            isCheck = 1
            half_topic += input[i]
        elif input[i] == '#' and isCheck == 1:
            isCheck = 0
            half_topic = ""
        elif isCheck == 0:
            output += input[i]
        elif isCheck == 1:
            half_topic += input[i]

    if isCheck == 1:
        output += half_topic

    return output


def filter_all(input):
    out1 = filter_username(input)
    out2 = filter_topic(out1)
    return out2


#---------------------------
# main
#---------------------------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: ./xxx.py input_file"
        exit(1)

    input_file = sys.argv[1]

    filter = SimhashFilter()
    filter.init_context()

    f = open(input_file, "r")

    while 1:
        lines = f.readlines(100000)
        if not lines:
            break

        for line in lines:
            l = line.replace('\n', '')
            if len(l) < 2:
                continue

            k = filter_all(l)
            v = l

            simhash = filter.get_simhash(k)
            ret = filter.is_exists(simhash)
            if ret == 0:
                print v

    f.close()

