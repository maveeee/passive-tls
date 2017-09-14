# BroAnalyzer

BroAnalyzer is a set of Python 2.7 scripts which help to extract and visualize information from Bro SSL log files and collected certificates.

The two main components of BroAnalyzer are the analyzer and the visualizer.  
The analyzer executes queries on the provided data and stores the extracted information in csv files. The visualizer takes these files and generates plots out of them.

## Usage

### Analyzer

Executing the analyzer requires to have the Bro data in place. The analyzer expects those files in a specified data directory in a special structure. The data directory needs to hold a folder for each day whose name is the date in the format 'YYYY-MM-DD'. This folder contains again two folders, one for the logs and one for the certificates (named 'logs' and 'certificates').

Apart from specifying the data directory, running the analyzer requires to define which queries should be executed. This can be done by either adding the `-a` parameter to execute all available queries, or by specifically defining the queries using their corresponding parameters. For more details use the `-h` switch to display a help message showing all available queries.

Finally the analyzer is executed by running 
```python
python .\src\broAnalyzer\analyzer.py -d [datadirectory] [queryoptions]
```

### Visualizer

The visualizer requires similar parameters as the analyzer. At first it needs the directory containing the previously extracted csv files with the parameter `-d`. Then similiar to specifying the query options of the analyzer, the plots, which should be generated, are defined.

```python
python .\src\broAnalyzer\visualizer.py -d [datadirectory] [plots]
```
## Input File Format
The analyzer is meant to operate on Bro SSL log files. However, the file format can be adapted by modifying the function `parseLogFiles` in `src/broAnalyzer/util/parser.py`. 

## Extending BroAnalyzer
BroAnalyzer is designed to be extensible, the plots and queries are defined in seperate classes in special packages and the application takes care of their execution.  

### Queries
The queries executed by BroAnalyzer are defined in the `queries` package located in `src/broAnalyzer/queries`.  
The application defines two base classes, one for queries operating on ssl log data (`LogEntryQuery`) and one for certificate data (`CertificateQuery`), both defined in `src/util/query`. Among others, these classes define the method `apply` which takes a pandas DataFrame as parameter containing query/certificate data. This method is responsible for processing the data of a single day. After the data for all days is processed, the analyzer calls the `reduce` function providing all previously extracted results returned by `apply`. The `reduce` function is meant to return a single DataFrame containing the condensed query information which is then written to a csv file by the analyzer.

### Plots
Analog to the queries, plots share a base class called `Plot` defined in `src/util/plot`. The most important method defined by it is `plot` which takes the input and output folder as parameter. When implementing this method, one has to take care of reading the required csv file, generating the plot and saving the file to the output folder.

## Requirements
BroAnalyzer requires Python 2.7 and moreover the following libraries:

matplotlib==2.0.0  
numpy==1.11.3  
pandas==0.19.2  
pyasn1==0.1.9  
pyOpenSSL==16.2.0  