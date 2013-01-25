import unittest
import convert
from os import remove

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_convertSalesforceToSFMR(self):
        sd = convert.SurveyData()
        datadictCSV = 'conversionSFMR.csv'
        surveyCSV = 'testdata/AthenaDataExportTest.csv'
        outputCSV = 'testdata/AthenaDataExportSFMR.csv'
        questions, headers = sd.convertData(surveyCSV, datadictCSV)
        sd.toCSV(outputCSV, questions, headers)
        # now read from the file and verify
        del sd
        sd = convert.SurveyData()
        sd.data, sd.headers = sd.getData(outputCSV)
        self.assertEqual(sd.data,[['123456789', 'IDXR123467891376', '+fVQO/nZB7ZEySUzAK5eU8LT88HuJr1vINRQnufsEtM=', 'JOHN', 'STEINBECK', '5/10/12', '9:15 AM', '5/29/12', '0', '1', '5', '196', '1', '3', '0', '1', '0', '0', '0', '3', '3', '0', '0', '6', '4', '1', '1', '1']])
        remove(outputCSV)

        # should raise an exception for an immutable sequence
        # self.assertRaises(TypeError, random.shuffle, (1,2,3))

if __name__ == '__main__':
    unittest.main()
