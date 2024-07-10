import os
import subprocess
import shutil


def delete_unlisted_entries(path, allowed_entries):
	try:
		# Get the list of all files and directories in the specified directory
		entries_list = os.listdir(path)
		
		# Convert allowed_entries to a set for efficient lookup
		allowed_set = set(allowed_entries)
		
		# Iterate over the entries and delete those not in the allowed list
		for entry in entries_list:
			entry_path = os.path.join(path, entry)
			if entry not in allowed_set:
				if os.path.isfile(entry_path) or os.path.islink(entry_path):
					os.remove(entry_path)
					print(f"Deleted file: {entry_path}")
				elif os.path.isdir(entry_path):
					os.rmdir(entry_path)
					print(f"Deleted directory: {entry_path}")
		
		print(f"Unlisted entries have been deleted from {path}")
	except Exception as e:
		print(f"An error occurred: {e}")


def create_exe_from_spec(spec_file_path):
	try:
		# Call PyInstaller with the .spec file
		result = subprocess.run(['pyinstaller', spec_file_path], capture_output=True, text=True)
		
		# Check if the process was successful
		if result.returncode == 0:
			print("Executable created successfully.")
		else:
			print("An error occurred during the creation of the executable.")
			print(result.stdout)
			print(result.stderr)
	except Exception as e:
		print(f"An error occurred: {e}")


def move_entries_to_folder(entries, destination_folder):
	# Ensure the destination folder exists
	if not os.path.exists(destination_folder):
		os.makedirs(destination_folder)
	
	try:
		for entry in entries:
			# Check if the entry exists
			if os.path.exists(entry):
				# Get the base name of the entry (file or directory name)
				entry_name = os.path.basename(entry)
				# Construct the destination path
				destination_path = os.path.join(destination_folder, entry_name)
				
				# Move the entry to the destination folder
				shutil.move(entry, destination_path)
				print(f"Moved {entry} to {destination_path}")
			else:
				print(f"Error: {entry} does not exist.")
	except Exception as e:
		print(f"An error occurred: {e}")


# files that must be in the _internal folder in order for QRCodeExtractor.exe to work
REQUIRED_ITEMS = [
	"base_library.zip",
	"certifi",
	"charset_normalizer",
	"contourpy",
	"Cython",
	"freetype.dll",
	"kiwisolver",
	"libcrypto-3.dll",
	"libffi-8.dll",
	"libjpeg-9.dll",
	"libmodplug-1.dll",
	"libogg-0.dll",
	"libopus-0.dll",
	"libopusfile-0.dll",
	"libpng16-16.dll",
	"libssl-3.dll",
	"libtiff-5.dll",
	"libwebp-7.dll",
	"lxml",
	"markupsafe",
	"msvcp140.dll",
	"MSVCR120.dll",
	"numpy",
	"numpy.libs",
	"PIL",
	"pyexpat.pyd",
	"pyinstaller-6.4.0.dist-info",
	"python312.dll",
	"pyzbar",
	"scipy",
	"scipy.libs",
	"SDL2.dll",
	"SDL2_image.dll",
	"SDL2_mixer.dll",
	"SDL2_ttf.dll",
	"select.pyd",
	"sqlite3.dll",
	"tcl",
	"tcl8",
	"tcl86t.dll",
	"tk",
	"tk86t.dll",
	"unicodedata.pyd",
	"VCOMP140.DLL",
	"vcruntime140.dll",
	"vcruntime140_1.dll",
	"yaml",
	"zlib1.dll",
	"_asyncio.pyd",
	"_bz2.pyd",
	"_ctypes.pyd",
	"_decimal.pyd",
	"_elementtree.pyd",
	"_hashlib.pyd",
	"_lzma.pyd",
	"_multiprocessing.pyd",
	"_overlapped.pyd",
	"_queue.pyd",
	"_socket.pyd",
	"_sqlite3.pyd",
	"_ssl.pyd",
	"_testbuffer.pyd",
	"_tkinter.pyd",
	"_uuid.pyd",
	"_wmi.pyd",
]


# Entries that will be moved into the release folder
RELEASE_ENTRIES = [
    'dist/QRCodeDataExtractor',
]
RELEASE_DESTINATION_FOLDER = ''         # same folder as installer
SPEC_PATH = "QRCodeDataExtractor.spec"  # same folder as installer
LIB_FOLDER_PATH = RELEASE_DESTINATION_FOLDER+"/_internal"

create_exe_from_spec(SPEC_PATH)
move_entries_to_folder(RELEASE_ENTRIES, RELEASE_DESTINATION_FOLDER)
delete_unlisted_entries(RELEASE_DESTINATION_FOLDER, REQUIRED_ITEMS)
