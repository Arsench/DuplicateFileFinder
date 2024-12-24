# Duplicate File Finder

This Python script helps you find duplicate files within a specified directory and moves them to a designated "check" directory. It generates a report listing the moved duplicate files.
This script can be used in Linux and MacOS as well.
## Functionality

The script does the following:

1.  **Scans a Directory:** It recursively traverses a root directory and all its subdirectories.
2.  **Finds Duplicates:** It calculates a hash (either MD5 or SHA256) of each file's content. If multiple files have the same hash, they are considered duplicates.
3.  **Moves Duplicates:** It moves all duplicate files to a specified "check" directory.
4.  **Generates a Report:** It creates a text report file listing the moved duplicate files and their original locations.
5.  **File Extension Filtering:** You can specify a comma-separated list of file extensions to check. By default, all files are checked.

## How to Use

1.  **Installation:**
     * Ensure you have Python 3.6+ installed.
     * Navigate to the project directory and Install required packages by running:
         ```bash
         pip install -r requirements.txt
         ```
2.  **Run the Script:**
     Open a command prompt or terminal, navigate to the directory where you saved `duplicate_finder.py`, and run the script using the following format:

     ```bash
     python duplicate_finder.py "C:\path\to\scan" "C:\path\to\check" [--hash <MD5|SHA256>] [--extensions <ext1,ext2,...>] [--report_file <filename.txt>]
     ```

     *   `"C:\path\to\scan"`: The root directory to scan for duplicates (enclose in double quotes if paths have spaces).
     *   `"C:\path\to\check"`: The directory where the duplicate files will be moved (enclose in double quotes if paths have spaces).
     *   `--hash <MD5|SHA256>` (optional): The hashing method to use (`MD5` or `SHA256`). The default is `SHA256`.
     *   `--extensions <ext1,ext2,...>` (optional): A comma-separated list of file extensions to include in the duplicate check. Default is checking all files.
         For example: `--extensions "jpg,jpeg,png"` or `--extensions "txt,log,csv"`
     *  `--report_file <filename.txt>` (optional): The name of the text file to be generated as a report. Default is  `duplicate_report.txt`

     **Example:**

     *   Scan all files in `C:\my_files` and move duplicates to `C:\check_duplicates`, use SHA256 and the default report file name.
         ```bash
         python duplicate_finder.py "C:\my_files" "C:\check_duplicates"
         ```
     *   Scan only JPEG images in  `C:\my_images` and move duplicates to `C:\check_images`, use MD5 hashing and a report name of `my_image_duplicates.txt`.
        ```bash
         python duplicate_finder.py "C:\my_images" "C:\check_images" --hash MD5 --extensions "jpg,jpeg" --report_file "my_image_duplicates.txt"
        ```
     *   Scan all files in `C:\my_files` and move duplicates to `C:\check_duplicates` with the report name of `report_files.txt`:
         ```bash
         python duplicate_finder.py "C:\my_files" "C:\check_duplicates" --report_file "report_files.txt"
         ```
 ## Important Notes

 *   The script *moves* the duplicate files. The originals will no longer be in their original location, they will be in the `check_directory`.
 *   If the check directory doesn't exist, the script will automatically create it.
 *   If no duplicates are found, the script will state it in the console and will not create any report.
 *    If errors occur while reading or moving files the script will print them to the console and write them into the report file, and the script will proceed to scan the next files.
 *   Always enclose paths with spaces in double quotes on the command line.
 *   The report file will be created in the current directory where the script is executed.
