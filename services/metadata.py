from datetime import datetime
from jinja2 import Template

METADATA_FORMATS = [
    {
        'metadataPrefix': 'oai_dc',
        'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
        'metadataNamespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/'
    },
    {
        'metadataPrefix': 'oai_datacite',
        'schema':'http://schema.datacite.org/meta/kernel-4.4/metadata.xsd',
        'metadataNamespace': 'http://datacite.org/schema/kernel-4'
    }
]


def validate_metadata_prefix(metadata_prefix):
    return any(fmt.get('metadataPrefix') == metadata_prefix for fmt in METADATA_FORMATS)


list_metadata_formats_template = """
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{{ response_date }}</responseDate>
    <request verb="ListMetadataFormats">
        {{ base_url }}
    </request>
    <ListMetadataFormats>
        {% for format in metadata_formats %}
        <metadataFormat>
            <metadataPrefix>{{ format.metadataPrefix }}</metadataPrefix>
            <schema>{{ format.schema }}</schema>
            <metadataNamespace>{{ format.metadataNamespace }}</metadataNamespace>
        </metadataFormat>
        {% endfor %}
    </ListMetadataFormats>
</OAI-PMH>
"""


def list_metadata(base_url):
    context = {
        "response_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_url": base_url,
        "metadata_formats": METADATA_FORMATS
    }

    template = Template(list_metadata_formats_template)
    response = template.render(context)
    return response

