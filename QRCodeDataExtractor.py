import json
import os

from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from urllib.parse import unquote
from kraken import binarization


def get_file_from_path(file_path):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1].lower()
    
    with open(file_path, 'rb') as file:
        file_data = file.read()

    data = {
        "name": unquote(file_name),
        "path_name": file_path,
        "extension": file_extension,
        "binary_data": file_data
    }

    return data


def get_qrcodes_data_from_png_images(pdf_pages_as_png):
    qr_data = []

    for page_number, png_page in enumerate(pdf_pages_as_png):
        if png_page.size == (0, 0):
            continue

        decoded_objects = decode(png_page, symbols=[ZBarSymbol.QRCODE])

        if len(decoded_objects) == 0 and len(qr_data) == 0:
            for i in range(12):
                decoded_objects = decode(enhance_image(png_page), symbols=[ZBarSymbol.QRCODE])
                if len(decoded_objects) != 0:
                    break

        for obj in decoded_objects:
            str_data = obj.data.decode("utf-8")
            qr_data.append({
                "page": page_number + 1,
                "original_data": str_data,
                "data_as_json": get_structured_qrcode_data(str_data),
                "type": obj.type,
                "area": obj.rect.width * obj.rect.height
            })

    return qr_data


def extract_qrcode_data_from_pdf(file_path: str, poppler_path: str):
    try:
        file_data = get_file_from_path(file_path)
    except OSError:
        return {"Success": False, "ErrorMessage": "No 'local_pdf.pdf' file found!"}

    if file_data["extension"] != ".pdf":
        return {"Success": False, "ErrorMessage": "File is not a PDF!"}

    pdf_pages_as_png = convert_from_path(file_path, poppler_path=poppler_path)

    qr_data = get_qrcodes_data_from_png_images(pdf_pages_as_png)

    if len(qr_data) == 0:
        return {"Success": False, "ErrorMessage": f"No QRCode was found in {file_data['name']}"}

    return {"Success": True, "data": qr_data}


def get_structured_qrcode_data(data: str):
    data_as_dictionary = {}
    for raw_info in data.split("*"):
        split = raw_info.split(":")
        key, value = split[0], ":".join(split[1:])
        data_as_dictionary[key] = value

    return data_as_dictionary


def enhance_image(image):
    enhanced_image = binarization.nlbin(image)
    return enhanced_image


pdf_file_path = "local_pdf.pdf"
poppler_data_path = "poppler/Library/bin"
result = extract_qrcode_data_from_pdf(pdf_file_path, poppler_data_path)

with open("qrcode_data.json", 'w') as json_file:
    json.dump(result, json_file, indent=4)
