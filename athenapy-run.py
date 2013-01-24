#!/usr/bin/python

from sys import argv
import convert

if __name__ == '__main__':
    if argv[1] == 'convert':
        sd = convert.SurveyData()
        datadictCSV = argv[2]
        surveyCSV = argv[3]
        outputCSV = argv[4]
        questions, headers = sd.convertData(surveyCSV, datadictCSV)
        sd.toCSV(outputCSV, questions, headers)
