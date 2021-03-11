import os
import sys
import argparse
import re
from collections import defaultdict, Counter

import numpy as np
import pandas as pd


Threshold = 0.10
Excludes = 'the this of shall with will be for only can no without on to by feel in a from able and between no are if each all has been that within when after'
#Excludes = 'the this of if'
ExcludeList = Excludes.split(' ')

class Computing():
    def __init__(self):
        pass

    @staticmethod
    def computeSimilarity(setA, setB):
        rtn = len(setA & setB) / (len(setA) + len(setB))
        return rtn


class TextDataProcessor():
    def __init__():
        pass

    @staticmethod
    def findTheKey(tmpStr):
        pattern = '([FNR]*[0-9]*).*'
        m = re.match(pattern, tmpStr)
        if m:
            key = m.group(1)
        else:
            raise ValueError('key value is not find, please have check!')
        return key

    @staticmethod
    def filterList(strList):
        rtnList = []
        for item in strList:
            if item.endswith('.') or item.endswith(':'):
                item = item[:-1]
            #if item in ExcludeList:
            #    continue
            rtnList.append(item)
        return rtnList

    @staticmethod
    def readFile(fpath):
        frDict = defaultdict()
        nfrDict = defaultdict()

        frList = []
        nfrList = []

        try:
            with open(fpath, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            print('file read failed!')
            print(e.message)

        for line in lines:
            if '\n' == line:
                continue

            tmpList = line.strip().split(': ')
            key = TextDataProcessor.findTheKey(tmpList[0])
            valList = tmpList[1].split(' ')
            valList = TextDataProcessor.filterList(valList)
            if key.startswith('FR'):
                frDict[key] = set(valList)
            elif key.startswith('NFR'):
                nfrDict[key] = set(valList)
            else:
                raise ValueError('unexpected key value: {}'.format(key))

        return frDict, nfrDict


def write2file(outDict, fpath):
    lines = []
    for key in outDict.keys():
        tmp = outDict[key]
        tmpList = []
        for elem in tmp:
            if elem > Threshold:
                tmpList.append(1)
            else:
                tmpList.append(0)
        #tmpList = tmp
        #tmpLine = '{},{:f},{:f},{:f}'.format(key, tmpList[0], tmpList[1], tmpList[2])
        tmpLine = key
        for item in tmpList:
            tmpLine = '{},{:d}'.format(tmpLine, item)
        lines.append(tmpLine)
    contents = '\n'.join(lines)
    contents = contents + '\n'

    with open(fpath, 'w') as f:
        f.write(contents)


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file path')
    parser.add_argument('-o', '--output', help='output file path')
    opts = parser.parse_args()
    return opts


def main(opts):
    frDict, nfrDict = TextDataProcessor.readFile(opts.input)

    rtn = defaultdict()
    for key in frDict.keys():
        elemList = []
        for key2 in nfrDict.keys():
            elem = Computing.computeSimilarity(frDict[key], nfrDict[key2])
            elemList.append(elem)
        rtn[key] = elemList

    write2file(rtn, opts.output)


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
