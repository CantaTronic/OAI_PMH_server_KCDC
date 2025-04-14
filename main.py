from fastapi import FastAPI, Query, UploadFile, status
from fastapi.responses import Response

from services.metadata import validate_metadata_prefix, list_metadata
from services.list_records import list_records
from services.list_identifiers import list_identifiers
from services.get_record import get_record
from services.error import error_response
from services.identify import identify
from services.save_file import save_file

from config import config

app = FastAPI()

BASE_URL = config.BASE_URL
REPOSITORY_NAME = config.REPOSITORY_NAME
ADMIN_EMAIL = config.ADMIN_EMAIL
EARLIEST_DATE_TIMESTAMP = config.EARLIEST_DATE_TIMESTAMP

ERROR_CODE_BAD_ARGUMENT = 'badArgument'
ERROR_CODE_BAD_VERB = 'badVerb'
ERROR_CODE_FORMAT = 'cannotDisseminateFormat'
ERROR_CODE_NO_ID = 'idDoesNotExist'
ERROR_CODE_NO_RECORDS = 'noRecordsMatch'
ERROR_CODE_NO_METADATA = 'noMetadataFormats'


@app.get("/oai", response_class=Response)
async def oai(
    verb: str = Query(..., description="OAI-PMH operation"),
    identifier: str | None = None,
    metadataPrefix: str | None = None,
    # set: str | None = None
):
    if verb == "Identify":
        response_data = identify(BASE_URL, REPOSITORY_NAME, ADMIN_EMAIL, EARLIEST_DATE_TIMESTAMP)

    elif verb == "ListMetadataFormats":
        response_data = list_metadata(BASE_URL)
    else:
        if not metadataPrefix:
            response_data = error_response(BASE_URL, verb, ERROR_CODE_NO_METADATA,
                                           f'Argument metadataPrefix required but not supplied.')
            return Response(content=response_data,
                            media_type="application/xml")
        if not validate_metadata_prefix(metadataPrefix):
            response_data = error_response(BASE_URL, verb, ERROR_CODE_FORMAT,
                                           f'The metadataPrefix {metadataPrefix} is not supported by this repository.')
            return Response(content=response_data,
                            media_type="application/xml")

        if verb == "ListIdentifiers":
            response_data = list_identifiers(BASE_URL, metadataPrefix)

        elif verb == "GetRecord":
            if not identifier:
                response_data = error_response(BASE_URL, verb, ERROR_CODE_BAD_ARGUMENT,
                                               'Argument identifier required but not supplied.')
                return Response(content=response_data,
                                media_type="application/xml")

            status, response_data = get_record(BASE_URL, metadataPrefix, identifier)
            if not status:
                response_data = error_response(BASE_URL, verb, ERROR_CODE_NO_ID, response_data)
        elif verb == 'ListRecords':
            status, response_data = list_records(BASE_URL, metadataPrefix)
            if not status:
                response_data = error_response(BASE_URL, verb, ERROR_CODE_NO_RECORDS, response_data)

        else:
            response_data = error_response(BASE_URL, verb, ERROR_CODE_BAD_VERB,
                                           'Illegal OAI verb')

    return Response(content=response_data,
                    media_type="application/xml")


@app.post("/add_record", response_class=Response)
async def api_add_record(
    file: UploadFile,
    metadataPrefix: str | None = None,
    identifier: str | None = None,
):
    if not validate_metadata_prefix(metadataPrefix):
        response_data = error_response(BASE_URL, 'AddRecord', ERROR_CODE_FORMAT,
                                       f'The metadataPrefix {metadataPrefix} is not supported by this repository.')
        return Response(content=response_data,
                        media_type="application/xml")

    await save_file(file, metadataPrefix, identifier)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




