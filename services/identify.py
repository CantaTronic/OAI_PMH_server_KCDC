import os
from datetime import datetime
from jinja2 import Template
from lxml import etree

identify_template = """
<oai:OAI-PMH xmlns:oai="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <oai:responseDate>{{ response_date }}</oai:responseDate>
    <oai:request verb="Identify">
        {{ base_url }}
    </oai:request>
    <oai:Identify>
        <oai:repositoryName>{{ repository_name }}</oai:repositoryName>
        <oai:baseURL>{{ base_url }}</oai:baseURL>
        <oai:protocolVersion>{{ protocol_version }}</oai:protocolVersion>
        <oai:adminEmail>{{ admin_email }}</oai:adminEmail>
        <oai:earliestDatestamp>{{ earliest_datestamp }}</oai:earliestDatestamp>
        <oai:deletedRecord>{{ deleted_record }}</oai:deletedRecord>
        <oai:granularity>{{ granularity }}</oai:granularity>
    </oai:Identify>
</oai:OAI-PMH>
"""


def identify(base_url, repository_name, admin_email, earliest_datestamp,
                               deleted_record="no", granularity="YYYY-MM-DDThh:mm:ssZ", protocol_version="2.0"):
    context = {
        "response_date": datetime.utcnow().isoformat() + "Z",
        "base_url": base_url,
        "repository_name": repository_name,
        "protocol_version": protocol_version,
        "admin_email": admin_email,
        "earliest_datestamp": earliest_datestamp,
        "deleted_record": deleted_record,
        "granularity": granularity,
    }

    template = Template(identify_template)
    return template.render(context)
