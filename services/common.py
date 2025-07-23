
import os
from datetime import datetime
from io import StringIO
from csv import DictReader
from lxml import etree


def extract_kcdc_tags(csv_string, identifier):
    md = {}
    f = StringIO(csv_string, newline='')
    for row in DictReader(f):
        if row['Identifier'] != identifier:
            continue
        if row['Key'] == 'UUID':
            continue
        if row['Position'] not in {'range from', 'range till'}:
            continue
        if row['Setup'] not in md:
            md[row['Setup']] = {}
        if row['Key'] not in md[row['Setup']]:
            md[row['Setup']][row['Key']] = {}
        if row['Position'] == 'range from':
            md[row['Setup']][row['Key']]['min'] = row['Value']
        else:
            md[row['Setup']][row['Key']]['max'] = row['Value']
    return md


NSMAP = {
    None: "http://www.openarchives.org/OAI/2.0/",
    'dc_kcdc_ext': 'urn:kit:iap:kcdc:extension-schema:wrapper',
    "dc": "http://purl.org/dc/elements/1.1/",
    "kcdc_preselects": "urn:kit:iap:kcdc:extension-schema:preselects"
}
BASE_XML_DIRECTORY = "md_xml"


def tag(parent, ns: str, tag: str, **kwargs) -> str:
    return etree.SubElement(parent, f"{{{NSMAP[ns]}}}{tag}", **kwargs)


def get_md_dc(metadata_prefix, identifier):
    xml_file_path = f'{BASE_XML_DIRECTORY}/{metadata_prefix}/{identifier}.xml'

    # if not os.path.isfile(xml_file_path):
        # return f'No item found with this identifier {identifier} ({xml_file_path})'
    with open(xml_file_path) as f:
        xml_string = f.read()
    md = []
    ns = {
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    root = etree.fromstring(xml_string)
    for elem in root.xpath('.//dc:*', namespaces=ns):
        # Remove the namespace from tag
        tag_name = etree.QName(elem).localname
        tag_text = elem.text.strip() if elem.text else None
        if tag_name == 'description' and tag_text.startswith('TechnicalInfo'):
            continue
        md.append((tag_name, tag_text))
    return md


def mk_record(
    parent,
    metadata_prefix: str,
    identifier: str,
    response_time: datetime,
    csv_string: dict,
):
    record = tag(parent, None, 'record')
    header = tag(record, None, 'header')
    tag(header, None, 'identifier').text = identifier
    tag(header, None, 'datestamp').text = response_time.strftime("%Y-%m-%d")

    md = tag(tag(record, None, 'metadata'), 'dc_kcdc_ext', 'dc_kcdc')

    # DC elements
    md_dc = get_md_dc(metadata_prefix, identifier)
    for k, v in md_dc:
        tag(md, 'dc', k).text = v

    # Custom elements
    md_kcdc = extract_kcdc_tags(csv_string, identifier.partition('.')[0])
    for k, v in md_kcdc.items():
        setup = tag(md, 'kcdc_preselects', k)
        for k1, v1 in v.items():
            t = tag(setup, 'kcdc_preselects', k1)
            if 'min' in v1:
                tag(t, 'kcdc_preselects', 'min').text = v1['min']
            if 'max' in v1:
                tag(t, 'kcdc_preselects', 'max').text = v1['max']
