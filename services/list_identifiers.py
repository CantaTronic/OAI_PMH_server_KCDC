import os
from jinja2 import Template
from datetime import datetime

from services.get_record import BASE_XML_DIRECTORY

list_identifiers_template = """
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{{ response_date }}</responseDate>
    <request verb="ListIdentifiers" metadataPrefix="{{ metadata_prefix }}">
        {{ base_url }}
    </request>
    <ListIdentifiers>
        {% for identifier in identifiers %}
        <header>
            <identifier>{{ identifier }}</identifier>
            <datestamp>{{ datestamp }}</datestamp>
        </header>
        {% endfor %}
    </ListIdentifiers>
</OAI-PMH>
"""


def get_identifiers_from_directory(directory):
    try:
        identifiers = sorted(
            os.path.splitext(file)[0]
            for file in os.listdir(directory)
            if file.endswith('.xml')
        )
        return identifiers
    except FileNotFoundError:
        return []


def list_identifiers(base_url, metadata_prefix):
    identifiers = get_identifiers_from_directory(f'{BASE_XML_DIRECTORY}/{metadata_prefix}')

    context = {
        "response_date": datetime.utcnow().isoformat() + "Z",
        "base_url": base_url,
        "metadata_prefix": metadata_prefix,
        "identifiers": identifiers,
        "datestamp": datetime.utcnow().date().isoformat(),
    }

    template = Template(list_identifiers_template)
    response = template.render(context)
    return response
