# README

This is a code repository of KCDC OAI-PMH server. It runs at

https://8b6a156d-d591-4f81-9b15-eabc675012bb.ka.bw-cloud-instance.org/

At the moment, it provides shallow metadata for KCDC's Preselected  datasets:

- Schema: Dublin Core Qualified
- Protocol: OAI-PMH
- metadataPrefix: oai_dc
- verbs: ‘ListMetadataFormats’, ‘ListIdentifiers’, ‘GetRecord’, ‘ListRecords’.

After the planned update in mid-May, it will provide extended records, according to the specific schemas provided in the folder 'xsd'.

Examples of extended records and more information about the server can be found in the folder 'docs'.
