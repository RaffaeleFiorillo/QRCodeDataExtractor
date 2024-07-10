import json
import os

from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from urllib.parse import unquote
from kraken import binarization
from PIL import Image


def get_qrcodes_data_from_images(pdf_pages_as_png):
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
                "originalData": str_data,
                "dataAsJson": get_structured_qrcode_data(str_data),
                "type": obj.type,
                "area": obj.rect.width * obj.rect.height
            })
    
    return qr_data


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


def extract_qrcode_data_from_pdf(pdf_path: str):
    try:
        pdf_pages_as_png = convert_from_path(pdf_path, poppler_path="poppler/Library/bin")
    except Exception as excp:
        return {"Success": False, "ErrorMessage": f"Error Converting {pdf_path} to PNGs: {excp}"}
    
    qr_data = get_qrcodes_data_from_images(pdf_pages_as_png)
    
    if len(qr_data) == 0:
        return {"Success": False, "ErrorMessage": f"No QRCode was found in {file_data['name']}"}
    
    return {"Success": True, "data": qr_data}


def extract_qrcode_data_from_image(image_path: str):
    try:
        image = Image.open(image_path)
    except OSError:
        return {"Success": False, "ErrorMessage": "File not found or unsupported image format!"}
    
    qr_data = get_qrcodes_data_from_images([image])
    
    if len(qr_data) == 0:
        return {"Success": False, "ErrorMessage": f"No QRCode was found in {image_path}"}
    
    return {"Success": True, "data": qr_data}


def get_file_data_from_path(path):
    file_name = os.path.basename(path)
    file_extension = os.path.splitext(file_name)[1].lower()
    
    data = {
        "name": unquote(file_name),
        "path_name": path,
        "extension": file_extension,
    }
    
    return data


def get_file_path_from_conf():
    try:
        with open("conf_file.txt", 'r') as txt_file:
            path = txt_file.readline().strip()
        
        # Empty the file after reading
        open("conf_file.txt", 'w').close()
        
        return path
    except OSError:
        return ""


file_path = get_file_path_from_conf()
file_data = get_file_data_from_path(file_path)

try:
    if file_data["path_name"] == "":
        result = {"Success": False, "ErrorMessage": f"No file specified for extraction."}
    elif file_data["extension"] == ".pdf":
        result = extract_qrcode_data_from_pdf(file_data["path_name"])
    elif file_data["extension"] in (".png", ".jpg", ".jpeg"):
        result = extract_qrcode_data_from_image(file_data["path_name"])
    else:
        result = {"Success": False, "ErrorMessage": f"Unsupported file extension {file_data['extension']}"}
except Exception as ex:
    result = {"Success": False, "ErrorMessage": f"Unespected Error tying to extract data from {file_data}: {ex}"}

with open("qrcode_data.json", 'w') as json_file:
    json.dump(result, json_file, indent=4)
