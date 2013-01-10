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
    f = open(fileName)
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

  def conversionToCSV(self, fileName, qs, headers):
    f = open(fileName, 'w')
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

#  Old code
#   def createDictFromSFMRcomparison(self, fileName, outFile=None):
#     def convertSFMRChoiceEntries(choices, coded_values, sfmr_choices_and_values):
#       sfmr_choice_values = []
#       for line in sfmr_choices_and_values.strip().split('\n'):
#         try:
#           choice, value = (line[:line.rindex('(')], line[(line.rindex('(') + 1) : ])
#         except ValueError:
#           print("Line unable to be parsed:\n%s\n from entry:\n%s" % (line, sfmr_choices_and_values))
#           raise
#         choice = choice.strip()
#         value = value.split(')')[0]
#         sfmr_choice_values.append((choice, value))
#       return sfmr_choice_values

#     if outFile is not None:
#       f = open(outFile, 'w')
#       w = csv.writer(f)

#     try:
#       data, headers = self.getData(fileName)
#       adict = {}
#       question = None
#       coded_value = None
#       # get the relevant variables (if blank don't overwrite the old ones
#       for entry in data:
#         if entry[9] is not '':
#           question = entry[9]
#         if entry[6] is not '':
#           answers = entry[6].strip().split('\n')
#         if entry[8] is not '':
#           coded_values = entry[8].strip().split('\n')
#         # if the entry doesn't have sfmr variables don't process it further
#         if entry[8] == '' or entry[14] == '':
#           if outFile is not None:
#             w.writerow(entry)
#           continue
#         # if the question has a numeric answer enter it as a tuple into the dictionary instead of a dict
#         if entry[5] == 'Numeric' and entry[14] is not None:
#           adict[question] = ('', 'value', entry[15])
#           if outFile is not None:
#             w.writerow(entry + ['value', entry[15], sfmr_variable_name])
#           continue
#         if entry[14] is not '':
#           sfmr_coded_values = convertSFMRChoiceEntries(answers, coded_values, entry[14])
#           sfmr_variable_name = entry[15]
#         else:
#           continue
#         anentry = {}
#         if len(answers) == 1 and len(coded_values) == 1:
#           anentry[answer] = list(sfmr_coded_values[0]) + [sfmr_variable_name]
#           if outFile is not None:
#             w.writerow(entry + [answers[0], coded_values[0]] + list(sfmr_coded_values[0]) + [sfmr_variable_name])
#           continue
#         hold_entry = entry
#         for answer, coded_value in zip(answers, coded_values):
#           sfmr_codes = [i[1] for i in sfmr_coded_values]
#           entry = hold_entry + [answer, coded_value]
#           if coded_value in sfmr_codes:
#             anentry[answer] = list(sfmr_coded_values[sfmr_codes.index(coded_value)]) + [sfmr_variable_name]
#             if outFile is not None:
#               w.writerow(entry + list(sfmr_coded_values[sfmr_codes.index(coded_value)]) + [sfmr_variable_name])
#           elif int(coded_value) > 0 and answer[:3].lower() == 'yes' and ('Yes', '1') in sfmr_coded_values:
#             anentry[answer] = ('Yes', '1', sfmr_variable_name)
#             if outFile is not None:
#               w.writerow(entry + ['Yes', '1', sfmr_variable_name])
#           else:
#             if outFile is not None:
#               w.writerow(entry + ['', '', sfmr_variable_name])
            
#         adict.setdefault(question, {}).update(anentry)
#     except:
#       raise
#       import sys
#       print sys.exc_info()[0]
#       import pdb; pdb.set_trace()
#     f.close()
#     return adict
