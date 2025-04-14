from fastapi import UploadFile

from services.get_record import BASE_XML_DIRECTORY


async def save_file(file: UploadFile, metadataPrefix: str, identifier: str) -> None:
    file_path = f'{BASE_XML_DIRECTORY}/{metadataPrefix}/{identifier}.xml'
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)