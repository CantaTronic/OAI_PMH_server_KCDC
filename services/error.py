from jinja2 import Template
from datetime import datetime


error_template = """
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{{ response_date }}</responseDate>
    <request verb="{{ verb }}">
        {{ base_url }}
    </request>
    <error code="{{ error_code }}">{{ error_message }}</error>
</OAI-PMH>
"""


def error_response(base_url, verb, error_code, error_message):
    context = {
        "response_date": datetime.utcnow().isoformat() + "Z",
        "base_url": base_url,
        "verb": verb,
        "error_code": error_code,
        "error_message": error_message,
    }
    template = Template(error_template)
    return template.render(context)
