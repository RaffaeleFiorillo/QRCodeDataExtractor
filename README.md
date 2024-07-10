# QRCodeDataExtractor
A simple tool to extract the data contained in a QRCode located inside a file.
When executed, "QRCodeDataExtraction.exe" uses a pdf (located in the same directory,with the name "local_pdf.pdf")
to create a json file with the data extracted from a QRCode (found inside the pdf).


# Requirements:
For the "QRCodeDataExtraction.exe" tool to work, the following items must be in the same directory:
	- "local_pdf.pdf";
	- "_internal": folder with all dependencies and libraries for the .exe to run;
	- "poppler": folder with the poppler tool, which you can donwload here: https://github.com/oschwartz10612/poppler-windows/releases/download/v24.02.0-0/Release-24.02.0-0.zip

Note: The downloaded poppler folder initially has a name like "poppler-24.02.0". You must rename the folder to be just "poppler".
This ensures that you can download and use the latest version without having to rebuild "QRCodeDataExtraction.exe". 


# How to use:
	1st-> put the pdf with the QRCode inside the directory;
	2nd-> Rename the pdf to "local_pdf.pdf";
	3rd-> run QRCodeDataExtraction.exe;

 
# Results Options:
Here is what can be found inside the json file when "QRCodeDataExtraction.exe" is executed:

## Case 1 - Correct execution and QRCode Found:


# How to Upgrade:
Create the .exe file based on the python code:
	pyinstaller QRCodeDataExtractor.spec

Install all required libraries for the code to work:
	pip install -r requirements.txt


