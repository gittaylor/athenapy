import csv
from datetime import datetime
from sys import exc_info

class SurveyData(object):

  sampleKey = {'question1':  {'NA': 0, '0': 0, '1': 1}}

  def __init__(self, fileName=None):
    if fileName is not None:
      self.data, self.headers = self.getData(fileName)
    self.conversions = {}

  def getData(self, fileName):
    f = open(fileName, 'rU')
    surveys = csv.reader(f)
    data = [i for i in surveys]
    f.close()

    headers = data.pop(0)
    return data, headers

  def createDictFromSFMRcomparison(self, fileName, options=None):  
    datadict = {}
    f = open(fileName, 'rU')
    if options is not None:
      r = csv.DictReader(f, **options)
    else:
      r = csv.DictReader(f)

    for entry in r:
      if not(entry['SFMR variable'] == ''):
        datadict.setdefault(entry['Variable'], {})[entry['Choice']] = (entry['SFMR variable'], entry['SFMR coded value'])
    return datadict

  def convert(self, adict=None):
    def appendVal(colname, transval, outputHeaders, outputrow):
      if colname in outputHeaders:
        outputrow[outputHeaders.index(colname)] = transval
      else:
        outputHeaders.append(colname)
        outputrow.append(transval)

    output = []
    outputHeaders = []
    errors = []
    if adict is None:
      adict = self.sampleKey
    for data in self.data:
      outputrow = ['' for i in range(len(outputHeaders))]
      for key in self.headers:
        if key in adict:
          index = self.headers.index(key)
          curkey = adict[key]
          val = data[index]
          if 'value' in curkey and curkey['value'][1] == 'value':
            # values that are to be translated literally are marked:  {'value': ('translated colummn', 'value')}
            colname = curkey['value'][0]
            try:
              num = int(val)
              appendVal(colname, num, outputHeaders, outputrow)
              continue
            except ValueError:
              try:
                num = float(val)
                appendVal(colname, num, outputHeaders, outputrow)
                continue
              except:
                # if this fails move on to the default value assignment below
                pass
            except:
              # if this fails move on to the value assignment below
              pass
          if 'string' in curkey and curkey['string'][1] == 'string':
            # strings that are to be kept are marked:  {'string': ('translated colummn', 'string')}
            appendVal(curkey['string'][0], val, outputHeaders, outputrow)

          # no elif needed here because if the value assignment fails it will default to the normal way of processing
          if val in curkey:
            colname, transval = curkey[val]
            appendVal(colname, transval, outputHeaders, outputrow)
            continue
          else:
            errors.append((data, val, curkey))
      output.append(outputrow)
    return output, outputHeaders, errors

  def convertSalesforceToSFMR(self, salesforceFilename, conversionSFMRFilename):
    def questionnaireKeyGenerator(mrn_index, cd_index, errors):
      def q_fxn(x):
        try:
          dateparts = x[cd_index].split('/')
          cd = datetime(dateparts[2], dateparts[1], dateparts[0])
        except:
          cd = datetime.now()
          errors.append(exc_info()[0])
        return (x[mrn_index], cd)
      return q_fxn

    self.data, self.headers = self.getData(salesforceFilename)
    self.sampleKey = self.createDictFromSFMRcomparison(conversionSFMRFilename)
    qs, headers, errors = self.convert()
    self.conversions.setdefault('convertSalesforceToSFMR', []).append({'questionnaires': qs, 'headers': headers, 'errors': errors})

    # Now return format the data to only return to SFMR the questionnaires they want in the sort order they want
    # sort by medical record number, return only the first entry for each patient (determined by MRN and CompletedDate, respectively)
    mrns = {}
    # find the index of the position of the mrn and the CompletedDate
    mrn_index = headers.index('MRN')
    cd_index = headers.index('CompletedDate')
    apptdate_index = headers.index('ApptDate')
    finalqs = []
    # sort the questionnaires by medical record number, completed date
    qs.sort(key=questionnaireKeyGenerator(mrn_index, cd_index, errors))
    for q in qs:
      # if there is not already a questionnaire for this individual and if the ApptDate is populated
      if not(q[mrn_index] in mrns) and not(q[apptdate_index] == ''):
        finalqs.append(q)
        mrns[q[mrn_index]] = None
    return finalqs, headers

  def toCSV(self, fileName, qs, headers):
    f = open(fileName, 'wb')
    w = csv.writer(f)
    w.writerow(headers)
    for q in qs:
      w.writerow(q)
    f.close()

  def getAllResponses(self):
    responses = {}
    for data in self.data:
      for i in self.headers:
        responses[i][data[self.headers[i]]] = responses.setdefault(i, {}).get(data[self.headers[i]],0) + 1
    return responses

  def graphAllResponses(self):

    from matplotlib import use as usedisplay
    usedisplay("Agg")
    from pylab import figure, barh, xticks, yticks, xlabel, ylabel, title, grid

    responses = self.getAllResponses
    fignum = 1
    for response in responses:
      figure(fignum)
      fignum += 1
      barh(pos,val, align='center')
      yticks(pos, )
    xlabel('Performance')
    title('How fast do you want to go today?')
    grid(True)

    figure(2)
    barh(pos,val, xerr=rand(5), ecolor='r', align='center')
    yticks(pos, ('Tom', 'Dick', 'Harry', 'Slim', 'Jim'))
    xlabel('Performance')
