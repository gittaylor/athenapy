from sys import argv
import convert

if __name__ == '__main__':
    if argv[1] == 'convert-Salesforce-SFMR':
        sd = convert.SurveyData()
        questions, headers = sd.convertSalesforceToSFMR(argv[3], argv[2])
        sd.toCSV(questions, headers)
        
