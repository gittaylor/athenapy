# athenapy Readme

## Description

A toolkit for developing and deploying Python applications for the [UC Athena](http://athenacarenetwork.org/) project.

## Requirements

An environment which includes Python (2.6 recommended)

## Usage

```bash
athenapy-run.py <function> <dataDict> <surveys> <outputFile>
```

example:

```bash
athenapy-run.py convertSalesforceToSFMR MySalesforceSFMRDict.csv MySurveys.csv MySFMRSurveys.csv
```

Depending on your environment, you may have to explicitly call the Python executable

Windows

```bash
/c/Python26/python.exe athenapy-run.py convertSalesforceToSFMR MySalesforceSFMRDict.csv MySurveys.csv MySFMRSurveys.csv
```

Linux

```bash
python2.6  athenapy-run.py convertSalesforceToSFMR MySalesforceSFMRDict.csv MySurveys.csv MySFMRSurveys.csv
```

## Testing

### Running Unit Tests

Windows

```bash
/c/Python26/python.exe tests.py
```

Linux

```bash
python2.6 tests.py
```