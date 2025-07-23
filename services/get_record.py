
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


def get_record(base_url, metadataPrefix, identifier):

    file_path = f'{BASE_XML_DIRECTORY}/expanded_ranges_with_position.csv'
    with open(file_path) as f:
        csv_string = f.read()

    return True, mk_xml(base_url, identifier, metadataPrefix, csv_string)


def mk_xml(
    base_url: str,
    identifier: str,
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
    request.set('verb', 'GetRecord')
    request.set('identifier', identifier)
    request.set('metadataPrefix', metadata_prefix)
    request.text = base_url

    body = tag(root, None, 'GetRecord')
    mk_record(body, metadata_prefix, identifier, response_time, csv_string)

    return etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8",
    ).decode()
