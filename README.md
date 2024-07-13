# QRCodeDataExtractor V2.1
A simple tool to extract the data contained in a QRCode located inside a file.
When executed, "QRCodeDataExtraction.exe" uses a pdf or image to create a json file with the data extracted from a QRCode (found inside the pdf).

# Requirements:
For the "QRCodeDataExtraction.exe" tool to work, the following items must be in the same directory:
	- "_internal": folder with all dependencies and libraries for the .exe to run;
	- "poppler": folder with the poppler tool, which you can donwload here: https://github.com/oschwartz10612/poppler-windows/releases/download/v24.02.0-0/Release-24.02.0-0.zip
 	- "conf_file.txt": File where you must write the name of the file you want to use for the extraction;
  	- "QRCodeDataExtraction.exe": The tool that does the extraction upon execution;

Note: The downloaded poppler folder initially has a name like "poppler-24.02.0". You must rename the folder to be just "poppler".
This ensures that you can download and use the latest version without having to rebuild "QRCodeDataExtraction.exe". 

# How to use:
	1st-> put the pdf with the QRCode inside the directory;
	2nd-> Rename the pdf to "local_pdf.pdf";
	3rd-> run QRCodeDataExtraction.exe;

# Results Options:
Here is what can be found inside the json file when "QRCodeDataExtraction.exe" is executed:

## Case 1 - Correct execution and QRCode Found:
    {
    "Success": boolean indicating if any QRCode was found,
    "data": [
        {
            "page": integer indicating in which page the QRCode was found (will always be one in non-pdf files),
            "originalData": "string with the scanned value of the QRCode",
            "dataAsJson": {
                "Field": "Value",
            },
            "type": "QRCODE",
            "area": integer indicating the are occupied by the QRCode (pixel*pixel),
	    "extractionTime": float representing how much time was spent extracting this QRCode,
	    "enhancementWasRequired": bool that shows if image enhancement was used to be able to extract the QRCode.
        }
    ]
    }
    
## Case 2 - "conf_file.txt" is left empty:
    {
    "Success": false,
    "ErrorMessage": "No file specified for extraction."
    }
    
## Case 3 - File not found in the path written inside "conf_file.txt":
    {
    "Success": false,
    "ErrorMessage": "File not found or unsupported image format!"
    }
## Case 4 - No QRCode was found:
    {
    "Success": false,
    "ErrorMessage": "No QRCode was found in *path of the file*"
    }
# How to Upgrade:
	1- Install all required libraries for the code to work:
		pip install -r requirements.txt
	2- Change the code inside QRCodeDataExtractor.py in a way that makes the tool work as you like
	3- Run ToolBuilder.exe
	4- The new version of the tool will be inside a folder called QRCodeDataExtractor
