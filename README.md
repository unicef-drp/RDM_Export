# RDM_Export
Export some data from RDM using RDM public APIs

**Note**: When exporting indicators, the API allows to access only indicators that are marked as "published" in RDM. If an indicator is not marked as "published", it will not be accessible through the 
API so it will not be seen by other tools (like Consult) and websites (like the Indicator Pages on data.unicef.org).

**Note**: The current script is mapping to Python objects and then CSV columns only the attributes that are currently used in RDM. Attributes that haven't been used yet or attributes that will be added in the future to RDM must be added to the Python object, to the API reader, and to the CSV exporter

## Advanced command line arguments
```
  -h, --help        Show the help message and exit
  --target          Required. Dataset to export: indicators, countries, regions
```

## Installation
Once you clone the GIT repository, requirements must be installed:
```
pip3 install -r requirements.txt
```
or
```
py -m pip install -r requirements.txt
```

If you don't have pip3 installed, you can install it with the commands:
```
sudo apt update  
sudo apt install python3-pip  
```

## Installation with virtual environment
To create a virtual environment:
```
py -m venv .venv 
.\.venv\Scripts\activate
deactivate
```
Once you clone the GIT repository, requirements must be installed:
```
pip3 install -r requirements.txt
```
or
```
py -m pip install -r requirements.txt
```

## Example of execution  
Note: the name of the executor depends on your environment. On Linux it is usually "python3", but in Windows it may just be "py".  

**Example:** For extracting all public indicators from RDM in CSV:

```
python3 main.py --target indicators
```
  
**Example:** For extracting all countries from RDM in CSV:

```
python3 main.py --target countries
```
  
**Example:** For extracting all regions from RDM in CSV:

```
python3 main.py --target regions
```