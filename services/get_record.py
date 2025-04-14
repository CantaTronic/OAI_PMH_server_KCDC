import os
from datetime import datetime
from jinja2 import Template
from lxml import etree

BASE_XML_DIRECTORY = "md_xml"

get_record_template = """
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
             xmlns:dc="http://purl.org/dc/elements/1.1/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{{ response_date }}</responseDate>
    <request verb="GetRecord" identifier="{{ identifier }}" metadataPrefix="{{ metadata_prefix }}">
        {{ base_url }}
    </request>
    <GetRecord>
        <record>
            <header>
                <identifier>{{ identifier }}</identifier>
                <datestamp>{{ datestamp }}</datestamp>
            </header>
            <metadata>
                {{ metadata | safe }}
            </metadata>
        </record>
    </GetRecord>
</OAI-PMH>
"""


def extract_metadata_from_file(xml_file_path):
    try:
        tree = etree.parse(xml_file_path)
        '''
        root = tree.getroot()
        dc_namespace = "http://purl.org/dc/elements/1.1/"
        etree.register_namespace("dc", dc_namespace)
        for elem in root.iter():
            elem.tag = f"{{{dc_namespace}}}{elem.tag.split('}')[-1]}"
        metadata_xml = etree.tostring(root, pretty_print=True, encoding="unicode")
        '''
        namespaces = {
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "dc": "http://purl.org/dc/elements/1.1/"
        }
        metadata_xml = tree.find(".//oai_dc:dc", namespaces=namespaces)
        metadata_xml = etree.tostring(metadata_xml, pretty_print=True, encoding="unicode")
        return metadata_xml
    except Exception as e:
        print(f"Ошибка при чтении XML: {e}")
        return ""


def get_record(base_url, metadataPrefix, identifier):

    xml_file_path = f'{BASE_XML_DIRECTORY}/{metadataPrefix}/{identifier}.xml'

    if not os.path.isfile(xml_file_path):
        return False, 'No item found with this identifier'

    metadata_content = extract_metadata_from_file(xml_file_path)

    context = {
        "response_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_url": base_url,
        "identifier": identifier,
        "metadata_prefix": metadataPrefix,
        "datestamp": datetime.utcnow().strftime("%Y-%m-%d"),
        "metadata": metadata_content
    }

    template = Template(get_record_template)
    response = template.render(context)

    return True, response


