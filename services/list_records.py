
import os
import re
from datetime import datetime

from lxml import etree

from services.common import (
    NSMAP,
    BASE_XML_DIRECTORY,
    tag,
    mk_record,
)


def get_identifiers_from_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".xml"):
            yield filename.rpartition('.')[0]


def list_records(base_url, metadataPrefix):

    file_path = f'{BASE_XML_DIRECTORY}/expanded_ranges_with_position.csv'
    with open(file_path) as f:
        csv_string = f.read()

    return True, mk_xml(base_url, metadataPrefix, csv_string)


def mk_xml(
    base_url: str,
    metadata_prefix: str,
    csv_string: dict,
) -> str:
    response_time = datetime.utcnow()

    root = etree.Element(
        f"{{{NSMAP[None]}}}OAI-PMH",
        nsmap=NSMAP,
    )

    tag(root, None, 'responseDate').text = response_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    request = tag(root, None, 'request')
    request.set('verb', 'ListRecords')
    request.set('metadataPrefix', metadata_prefix)
    request.text = base_url

    body = tag(root, None, 'ListRecords')
    for identifier in get_identifiers_from_directory(f'{BASE_XML_DIRECTORY}/{metadata_prefix}'):
        mk_record(body, metadata_prefix, identifier, response_time, csv_string)

    return etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8",
    ).decode()
