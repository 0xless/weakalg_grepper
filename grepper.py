import re
import json
import os
import traceback

# Function to recursively traverse directories and files and apply regex matching
def traverse_directory(path, regex_dict):
    results = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r') as f:
                for i, line in enumerate(f, start=1):
                    for regex in regex_dict:
                        x = regex_dict[regex]["regex"]
                        for r in x:
                            if re.match(r, line, re.IGNORECASE):
                                result = {
                                    "file": file_path,
                                    "line_number": i,
                                    "name": regex_dict[regex]["name"],
                                    "description": regex_dict[regex]["description"],
                                    "line": line
                                }
                                results.append(result)
            
        for dir in dirs:
            traverse_directory(os.path.join(root, dir), regex_dict)  # Recursively call traverse_directory on subdirectories
    return results

# Load regex expressions from JSON file
with open('regex.json', 'r') as f:
    regex_dict = json.load(f)

# Traverse through directories and files to apply regex matching
results = traverse_directory('/home/less/Documents/pentest/vitesco/SCR_DQ/DQ400_CFD/Bootsector/TC37x_SBoot/source/boot/crypto/src', regex_dict)

# Write results to text file
with open('regex_matches.txt', 'w') as f:
    for result in results:
        f.write(f"Name: {result['name']} | File: {result['file']}:{result['line_number']} | Description: {result['description']} | Line: {result['line']}\n")

print("Done!")