import os
import re
from datetime import datetime
from jinja2 import Template
from lxml import etree

from services.get_record import BASE_XML_DIRECTORY

list_records_template = """
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
         xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
                             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd
                             http://www.openarchives.org/OAI/2.0/oai_dc/
                             http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
    <responseDate>{{ response_date }}</responseDate>
    <request verb="ListRecords" metadataPrefix="{{ metadata_prefix }}">
        {{ base_url }}
    </request>
    <ListRecords>
        {% for record in records %}
        <record>
            <header>
                <identifier>{{ record.identifier }}</identifier>
                <datestamp>{{ record.datestamp }}</datestamp>
            </header>
            <metadata>
                {{ record.metadata | safe }}
            </metadata>
        </record>
        {% endfor %}
    </ListRecords>
</OAI-PMH>
"""


def extract_records_from_directory(directory_path):
    records = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory_path, filename)
            try:
                tree = etree.parse(file_path)
                '''
                root = tree.getroot()
                dc_namespace = "http://purl.org/dc/elements/1.1/"
                etree.register_namespace("dc", dc_namespace)
                oai_dc_namespace = "http://www.openarchives.org/OAI/2.0/oai_dc/"
                etree.register_namespace("oai_dc", oai_dc_namespace)

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
                metadata_xml = re.sub(r'<oai_dc:dc .+?>', r'<oai_dc:dc>', metadata_xml)

                record = {
                    "identifier": tree.find(".//identifier").text if tree.find(".//identifier") is not None else "Unknown",
                    "datestamp": tree.find(".//datestamp").text if tree.find(".//datestamp") is not None else "2024-01-01",
                    "metadata": metadata_xml,
                }
                records.append(record)
            except Exception as e:
                print(f"Ошибка при чтении файла {filename}: {e}")
    return records


def list_records(base_url, metadataPrefix):

    records = extract_records_from_directory(f'{BASE_XML_DIRECTORY}/{metadataPrefix}')
    if not records:
        return False, 'No records found'

    context = {
        "response_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_url": base_url,
        "metadata_prefix": metadataPrefix,
        "records": records,
    }

    template = Template(list_records_template)
    response = template.render(context)
    return True, response


