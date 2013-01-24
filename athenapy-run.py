#!/usr/bin/python

from sys import argv
import convert

if __name__ == '__main__':
    if argv[1] == 'convertSalesforceToSFMR':
        sd = convert.SurveyData()
        datadictCSV = argv[2]
        surveyCSV = argv[3]
        outputCSV = argv[4]
        questions, headers = sd.convertSalesforceToSFMR(surveyCSV, datadictCSV)
        sd.toCSV(outputCSV, questions, headers)

        
