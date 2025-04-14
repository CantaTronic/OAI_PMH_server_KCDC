import os
from datetime import datetime
from jinja2 import Template
from lxml import etree

from services.get_record import BASE_XML_DIRECTORY

list_records_template = """
<oai:OAI-PMH xmlns:oai="http://www.openarchives.org/OAI/2.0/"
             xmlns:dc="http://purl.org/dc/elements/1.1/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <oai:responseDate>{{ response_date }}</oai:responseDate>
    <oai:request verb="ListRecords" metadataPrefix="{{ metadata_prefix }}">
        {{ base_url }}
    </oai:request>
    <oai:ListRecords>
        {% for record in records %}
        <oai:record>
            <oai:header>
                <oai:identifier>{{ record.identifier }}</oai:identifier>
                <oai:datestamp>{{ record.datestamp }}</oai:datestamp>
                <oai:setSpec>{{ record.set_spec }}</oai:setSpec>
            </oai:header>
            <oai:metadata>
                {{ record.metadata | safe }}
            </oai:metadata>
        </oai:record>
        {% endfor %}
    </oai:ListRecords>
</oai:OAI-PMH>
"""


def extract_records_from_directory(directory_path):
    records = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory_path, filename)
            try:
                tree = etree.parse(file_path)
                root = tree.getroot()
                dc_namespace = "http://purl.org/dc/elements/1.1/"
                etree.register_namespace("dc", dc_namespace)

                for elem in root.iter():
                    elem.tag = f"{{{dc_namespace}}}{elem.tag.split('}')[-1]}"

                metadata_xml = etree.tostring(root, pretty_print=True, encoding="unicode")

                record = {
                    "identifier": root.find(".//identifier").text if root.find(".//identifier") is not None else "Unknown",
                    "datestamp": root.find(".//datestamp").text if root.find(".//datestamp") is not None else "2024-01-01",
                    "metadata": metadata_xml,
                }
                records.append(record)
            except Exception as e:
                print(f"Ошибка при чтении файла {filename}: {e}")
    return records


def list_records(base_url, metadataPrefix):

    records = extract_records_from_directory(BASE_XML_DIRECTORY)
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


