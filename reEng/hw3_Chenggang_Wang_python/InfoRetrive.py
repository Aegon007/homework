import os
import sys
import argparse
import re
from collections import defaultdict, Counter

import numpy as np
import pandas as pd



class Computing():
    def __init__(self):
        pass

    @staticmethod
    def computeSimilarity(vecA, vecB):
        vecA = np.array(vecA)
        vecB = np.array(vecB)
        rtn = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        rtn = 0.5 + 0.5 * rtn
        return rtn

    @staticmethod
    def computeTermFrequency(fileDict, vocabularyList):
        rtnDict = defaultdict()
        for key in fileDict.keys():
            doc_x = fileDict[key]
            termCounter = Counter(doc_x)
            counts = len(doc_x)
            oneFileDict = defaultdict()
            for term in vocabularyList:
                if term in termCounter.keys():
                    oneFileDict[term] = termCounter[term]/counts
                else:
                    oneFileDict[term] = 0
            rtnDict[key] = oneFileDict

        return rtnDict;

    @staticmethod
    def computeInverseDocFrequency(fileDict, vocabularyList):
        rtnDict = defaultdict()
        fileNum = len(fileDict.keys())
        for word in vocabularyList:
            count = 0
            for key in fileDict.keys():
                if word in fileDict[key]:
                    count = count + 1
            idf_val = np.log2(fileNum/count)
            rtnDict[word] = idf_val
        return rtnDict

    @staticmethod
    def getVocabularyList(fileDict):
        tmpSet = set()
        for tmpList in fileDict.values():
            tmpSet.update(tmpList)
        return list(tmpSet)

    @staticmethod
    def computeVector(file_x, vocabularyList, tfDict, idfDict):
        tmpVec = []
        for word in vocabularyList:
            tf_val = tfDict[file_x][word]
            idf_val = idfDict[word]
            w_i = tf_val * idf_val
            tmpVec.append(w_i)
        return tmpVec

    @staticmethod
    def vectorizeDocuments(fileDict):
        frDict = defaultdict()
        nfrDict = defaultdict()

        vocabularyList = Computing.getVocabularyList(fileDict)
        tfDict = Computing.computeTermFrequency(fileDict, vocabularyList)
        idfDict = Computing.computeInverseDocFrequency(fileDict, vocabularyList)

        for file_x in fileDict.keys():
            vec_x = Computing.computeVector(file_x, vocabularyList, tfDict, idfDict)
            if file_x.startswith('FR'):
                frDict[file_x] = vec_x
            elif file_x.startswith('NFR'):
                nfrDict[file_x] = vec_x
            else:
                raise ValueError('unexpected key value {} received'.format(file_x))

        return frDict, nfrDict


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
            if item.endswith('.'):
                item = item[:-1]
            rtnList.append(item)
        return rtnList

    @staticmethod
    def readFile(fpath):
        fileDict = defaultdict()

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
            fileDict[key] = valList

        return fileDict


def write2file(outDict, fpath):
    lines = []
    for key in outDict.keys():
        tmp = outDict[key]
        maxVal = np.max(tmp)
        tmpList = []
        for elem in tmp:
            if maxVal == elem:
                tmpList.append(1)
            else:
                tmpList.append(0)
        tmpLine = '{},{:d},{:d},{:d}'.format(key, tmpList[0], tmpList[1], tmpList[2])
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
    fileDict = TextDataProcessor.readFile(opts.input)
    frDict, nfrDict = Computing.vectorizeDocuments(fileDict)

    rtn = defaultdict()
    for key in frDict.keys():
        elem1 = Computing.computeSimilarity(frDict[key], nfrDict['NFR1'])
        elem2 = Computing.computeSimilarity(frDict[key], nfrDict['NFR2'])
        elem3 = Computing.computeSimilarity(frDict[key], nfrDict['NFR3'])
        rtn[key] = [elem1, elem2, elem3]

    write2file(rtn, opts.output)


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
