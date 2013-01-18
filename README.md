# athenapy Readme

## Description

athenapy is a toolkit for developing and deploying python applications for the [UC Athena](http://athenacarenetwork.org/) project

## Usage

```bash
athenapy-run.py <function> <dataDict> <surveys> <outputFile>

athenapy-run.py convertSalesforceToSFMR MySalesforceSFMRDict.csv MySurveys.csv MySFMRSurveys.csv

```

## Testing

### Running Unit Tests

From Windows
```bash
/c/Python26/python.exe tests.py
```

From Linux
```bash
python2.6 tests.py
```