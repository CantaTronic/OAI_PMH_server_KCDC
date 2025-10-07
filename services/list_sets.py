import os
from jinja2 import Template
from datetime import datetime

from services.get_record import BASE_XML_DIRECTORY
from services.common import get_identifiers_from_directory, get_sets

list_sets_template = """
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{{ response_date }}</responseDate>
    <request verb="ListSets">
        {{ base_url }}
    </request>
    <ListSets>
        {% for set in sets %}
        <set>
            <setSpec>experimental:{{ set }}</setSpec>
            <setName>Experimental Data from {{ set }}</setName>
        </set>
        {% endfor %}
    </ListSets>
</OAI-PMH>
"""


def list_sets(base_url):
    sets = get_sets(BASE_XML_DIRECTORY)

    context = {
        "response_date": datetime.utcnow().isoformat() + "Z",
        "base_url": base_url,
        "sets": sets,
    }

    template = Template(list_sets_template)
    response = template.render(context)
    return response
