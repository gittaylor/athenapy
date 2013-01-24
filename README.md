# athenapy Readme

## Description

A toolkit for developing and deploying Python applications for the [UC Athena](http://athenacarenetwork.org/) project.

## Requirements

An environment which includes Python (2.6 recommended). Git is recommended for development.

## Installation

```bash
git clone http://github.com/gittaylor/athenapy.git
cd athenapy
```

## Usage

```bash
athenapy-run.py <function> <data dictionary file> <survey data file> <output file>
```

example:

```bash
athenapy-run.py convert conversionSFMR.csv AthenaDataExport.csv AthenaDataExportSFMR.csv
```

Depending on your environment, you may have to explicitly call the Python executable

Windows

```bash
/c/Python26/python.exe athenapy-run.py convert conversionSFMR.csv AthenaDataExport.csv AthenaDataExportSFMR.csv
```

Linux

```bash
python2.6  athenapy-run.py convert conversionSFMR.csv AthenaDataExport.csv AthenaDataExportSFMR.csv
```

or (if your Linux system only has Python 2.6 installed)

```bash
python  athenapy-run.py convert conversionSFMR.csv AthenaDataExport.csv AthenaDataExportSFMR.csv
```

This call method will be used for the rest of the examples here.

## Testing

### Running Unit Tests

Linux

```bash
python tests.py
```

### Testing With A Salesforce Export

Log into your Athena Salesforce instance, and go to the Questionnaire Data Export page.

Choose Export Options: All Participant Data and Questionnaire Responses

Choose starting and ending dates (exports are limited to a certain number of surveys, so this may have to be a short period)

Leave all other defaults as they are (Local file name, Delimiter)

Click Export

You will be asked to save a file called AthenaDataExport.csv. Save it in the same location as you installed athenapy above.

Now try the following commands to convert the survey data

To SFMR format:

```bash
python athenapy-run.py convert testdata/conversionSFMR.csv AthenaDataExport.csv AthenaDataExportSFMR.csv 
```

To CDCG format:

```bash
python athenapy-run.py convert testdata/conversionCDCG.csv AthenaDataExport.csv AthenaDataExportCDCG.csv 
```