# RDM_Export
Export some data from RDM using RDM public APIs

**Note**: When exporting indicators, the API allows to access only indicators that are marked as "published" in RDM. If an indicator is not marked as "published", it will not be accessible through the 
API so it will not be seen by other tools (like Consult) and websites (like the Indicator Pages on data.unicef.org).

**Note**: The current script is mapping to Python objects and then CSV columns only the attributes that are currently used in RDM. Attributes that haven't been used yet or attributes that will be added in the future to RDM must be added to the Python object, to the API reader, and to the CSV exporter