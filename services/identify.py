import os
from datetime import datetime
from jinja2 import Template
from lxml import etree

identify_template = """
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{{ response_date }}</responseDate>
    <request verb="Identify">
        {{ base_url }}
    </request>
    <Identify>
        <repositoryName>{{ repository_name }}</repositoryName>
        <baseURL>{{ base_url }}</baseURL>
        <protocolVersion>{{ protocol_version }}</protocolVersion>
        <adminEmail>{{ admin_email }}</adminEmail>
        <earliestDatestamp>{{ earliest_datestamp }}</earliestDatestamp>
        <deletedRecord>{{ deleted_record }}</deletedRecord>
        <granularity>{{ granularity }}</granularity>
    </Identify>
</OAI-PMH>
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
