import os
import subprocess
import shutil


def delete_build_dist():
	try:
		# Delete build folder if it exists
		if os.path.exists('build'):
			shutil.rmtree('build')
			print("Deleted build folder.")
		
		# Delete dist folder if it exists
		if os.path.exists('dist'):
			shutil.rmtree('dist')
			print("Deleted dist folder.")
	except Exception as e:
		print(f"An error occurred while deleting build/dist folders: {e}")
		

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
					shutil.rmtree(entry_path)
					print(f"Deleted directory: {entry_path}")
		
		print(f"Unlisted entries have been deleted from {path}")
	except Exception as e:
		print(f"An error occurred: {e}")


def create_exe_from_spec(spec_file_path):
	try:
		# Call PyInstaller with the .spec file
		result = subprocess.run(['pyinstaller', spec_file_path],
		                        capture_output=True,
		                        shell=True,
		                        text=True)
		
		# Check if the process was successful
		if result.returncode == 0:
			print("Executable created successfully.")
		else:
			print("An error occurred during the creation of the executable.")
			print(result.stdout)
			print(result.stderr)
	except Exception as e:
		print(f"An error occurred: {e}")


def copy_folder(source_folder, destination_folder):
	try:
		# Check if the source folder exists
		if not os.path.exists(source_folder):
			print(f"Error: Source folder '{source_folder}' does not exist.")
			return
		
		# Create destination folder if it doesn't exist
		if not os.path.exists(destination_folder):
			os.makedirs(destination_folder)
		
		# Copy the contents of the source folder to the destination folder
		shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)))
		
		print(f"Folder '{source_folder}' copied successfully to '{destination_folder}'.")
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
	'dist/QRCodeDataExtractor/_internal',
	'dist/QRCodeDataExtractor/QRCodeDataExtractor.exe',
]
RELEASE_DESTINATION_FOLDER = 'QRCodeExtractorV2.0'  # folder where the release is created
SPEC_PATH = "QRCodeDataExtractor.spec"  # same folder as installer
LIB_FOLDER_PATH = RELEASE_DESTINATION_FOLDER + "/_internal"
CONFIG_TXT_FILE = RELEASE_DESTINATION_FOLDER + "/conf_file"

print("Deleting previous Tool Version ------------------------------------------------------------------------")
if os.path.exists(RELEASE_DESTINATION_FOLDER):
	shutil.rmtree(RELEASE_DESTINATION_FOLDER)
print("Deleting existing dist and build folders --------------------------------------------------------------")
delete_build_dist()  # delete the folders containing previous installations files
print("Creating executable and dependencies (may take some time) ---------------------------------------------")
create_exe_from_spec(SPEC_PATH)  # create the release files
print("Moving files to Distribution Directory ----------------------------------------------------------------")
move_entries_to_folder(RELEASE_ENTRIES, RELEASE_DESTINATION_FOLDER)  # move release files to release folder
print("Moving Poppler to Distribution Directory --------------------------------------------------------------")
copy_folder("poppler", RELEASE_DESTINATION_FOLDER)
print("Deleting Obsolete Dependencies---------- --------------------------------------------------------------")
delete_unlisted_entries(LIB_FOLDER_PATH, REQUIRED_ITEMS)  # delete all files not required for the tool to work
print("Deleting dist and build folders -----------------------------------------------------------------------")
delete_build_dist()  # delete the now obsolete folders created during installation
print("Creating conf_file.txt  -------------------------------------------------------------------------------")
with open(CONFIG_TXT_FILE, "w") as file:
	pass

input("Tool Update Complete. If no error occurred, the new release should be ready. (Press any button to Finish)")
