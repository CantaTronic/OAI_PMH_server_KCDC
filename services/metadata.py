from datetime import datetime
from jinja2 import Template

METADATA_FORMATS = [
    {
        'metadataPrefix': 'oai_dc',
        'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
        'metadataNamespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/'
    }
]


def validate_metadata_prefix(metadata_prefix):
    return any(fmt.get('metadataPrefix') == metadata_prefix for fmt in METADATA_FORMATS)


list_metadata_formats_template = """
<oai:OAI-PMH xmlns:oai="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <oai:responseDate>{{ response_date }}</oai:responseDate>
    <oai:request verb="ListMetadataFormats">
        {{ base_url }}
    </oai:request>
    <oai:ListMetadataFormats>
        {% for format in metadata_formats %}
        <oai:metadataFormat>
            <oai:metadataPrefix>{{ format.metadataPrefix }}</oai:metadataPrefix>
            <oai:schema>{{ format.schema }}</oai:schema>
            <oai:metadataNamespace>{{ format.metadataNamespace }}</oai:metadataNamespace>
        </oai:metadataFormat>
        {% endfor %}
    </oai:ListMetadataFormats>
</oai:OAI-PMH>
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

