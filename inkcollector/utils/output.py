import csv
import json

def friendly_filepath(filepath):
    """
    Format the output file path to be file-system friendly including the subdirectories
    
    Parameters:
    - filepath: The file path to format.
    
    Returns:
    - str: The formatted file path.
    """
    # Split the filepath into filename and file directory
    filename = filepath.split("/")[-1]
    filedir = "/".join(filepath.split("/")[:-1])

    # Remove any leading or trailing whitespace
    filename = filename.strip()
    
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")

    # Ensure the filename is file-system friendly
    filepath = ''.join(e for e in filename if e.isalnum() or e in ['_', '-', '.'])

    # Ensure the file directory is file-system friendly
    filedir = ''.join(e for e in filedir if e.isalnum() or e in ['\\','/'])

    # Join the filename and file directory
    filepath = f"{filedir}/{filename}"

    return filepath.lower()

def output_json(data, filename):
    """
    Save JSON data to a JSON file.

    Parameters:
    - data: The data to save (should be a dictionary or list).
    - filename: The name of the file to save the data to.

    Returns:
    - None
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def output_csv(data, filename):
    """
    Save data to a CSV file.

    Parameters:
    - data: The data to save (should be a list of dictionaries).
    - filename: The name of the file to save the data to.

    Returns:
    - None
    """

    if not data:
        return

    # Get the keys from the first dictionary in the list
    keys = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


    