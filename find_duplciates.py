import os
import hashlib
import shutil
import argparse
from tqdm import tqdm

def find_duplicate_files(root_dir, check_dir, hash_method="SHA256", extensions=None, report_file="duplicate_report.txt"):
    """
    Finds and moves duplicated files to the check_dir and creates a report.

    Args:
        root_dir (str): The starting directory to search for duplicates.
        check_dir (str): The directory to move the duplicated files to.
        hash_method (str, optional): The hashing algorithm to use ('MD5' or 'SHA256'). Defaults to 'SHA256'.
        extensions (list of str, optional): A list of file extensions to check (e.g., ['jpg', 'jpeg', 'png']).
            If None defaults to ['all'] which means all extensions
        report_file (str, optional): The name of the report file to be generated. Defaults to 'duplicate_report.txt'.
    """

    # Create the CHECK directory if it doesn't exist
    if not os.path.exists(check_dir):
        os.makedirs(check_dir)

    hashes = {}          # Dictionary to store file hashes and their paths
    duplicate_files = [] # List to store duplicated files

    total_files = 0
    # Count all the files in the directory to show the progress bar
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file ends with the provided extensions or if all files should be checked
            if extensions == ["all"] or any(filename.lower().endswith(ext) for ext in extensions):
                total_files += 1


    with tqdm(total=total_files, desc="Scanning files", unit="file") as pbar:
        # Iterate through all files in the root directory and its subdirectories
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                # Check if the file ends with the provided extensions or if all files should be checked
                if extensions == ["all"] or any(filename.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(dirpath, filename)  # Get full file path

                    try:
                        with open(file_path, "rb") as file:
                             file_content = file.read() # Read file content

                            # Calculate the file hash depending on the specified method
                            if hash_method == "MD5":
                                file_hash = hashlib.md5(file_content).hexdigest()
                            elif hash_method == "SHA256":
                                file_hash = hashlib.sha256(file_content).hexdigest()
                            else:
                                raise ValueError(f"Invalid hash method: {hash_method}")
                    except Exception as e:
                        print(f"Error reading file: {file_path} - {e}")
                        pbar.update(1) # Update progress bar on error reading
                        continue  # Skip to next file

                    # If hash exists it means that we have a duplicated file
                    if file_hash in hashes:
                        duplicate_files.append((file_path, hashes[file_hash])) # Add to duplicate files list
                    else:
                        hashes[file_hash] = file_path # Add hash and file path to the hashes dictionary
                    pbar.update(1) # Update the progress bar for each processed file


    if not duplicate_files:
        print("No Duplicate Files Found")
        return

    print("Duplicate Files Found, creating report...")

    # Create the output report
    with open(report_file, 'w') as outfile:
        for duplicate, original in duplicate_files:
             try:
                # Move files to the check directory
                shutil.move(
                    duplicate, os.path.join(check_dir, os.path.basename(duplicate))
                 )
                outfile.write(f"- Duplicate: {duplicate} (Original: {original}) - Moved\n")
             except Exception as e:
                outfile.write(f"- Error moving: {duplicate} {e}\n")
                print(f"- Error moving: {duplicate} {e}")

    print(f"Report created at: {os.path.abspath(report_file)}") # Notify where the output report is created

if __name__ == "__main__":
    # Create a ArgumentParser object to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Find duplicate files and move them to a check folder."
    )
    # Add arguments to the parser
    parser.add_argument(
        "root_directory",
        type=str,
        help="The starting directory for your scan",
    )
    parser.add_argument(
        "check_directory",
        type=str,
        help="The path for where the CHECK files will go",
    )
    parser.add_argument(
        "--hash",
        type=str,
        default="SHA256",
        choices=["MD5", "SHA256"],
        help="The hash method to use (MD5 or SHA256)",
    )
    parser.add_argument(
        "--extensions",
        type=str,
        default="all",
        help="Comma separated list of file extensions to check (e.g. 'jpg,jpeg,png'). Default is 'all'",
    )
    parser.add_argument(
        "--report_file",
        type=str,
        default="duplicate_report.txt",
        help="Name of the report file to be generated",
    )

    # Parse command-line arguments
    args = parser.parse_args()
    # Create a list with the extensions to filter if the parameter is not equals to "all"
    extensions_list = [ext.strip().lower() for ext in args.extensions.split(",")] if args.extensions != "all" else ["all"]
    # Call main function to find duplicated files
    find_duplicate_files(
        args.root_directory, args.check_directory, args.hash, extensions_list, args.report_file
    )