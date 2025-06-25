"""
This script iterates all folders under current path, and for each ".ly" file, remove its associated PDF and MIDI files,
and execute LilyPond command to re-generate them.
"""
import os
import subprocess
import json
from collections import defaultdict

LILYPOND_PATH = 'D:/Programs/lilypond-2.24.3/bin/lilypond.exe'

EXCLUDE_DIRS = ['snippet']
EXCLUDE_FILES = ['base.ly', 'template.ly', 'template_snippet.ly']

SHEET_JSON = 'sheet.json'

def refresh():
    sheets = defaultdict(list)

    for path, dirs, files in os.walk(os.getcwd()):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDE_DIRS]  # Skip dirs starting with "."
        for file in files:
            if file.endswith('.ly') and file not in EXCLUDE_FILES:
                name = os.path.splitext(file)[0]
                refresh_sheet(path, name)

                category = os.path.basename(path)
                sheets[category].append(name)

    # Export the collected map to sheet.json
    with open(SHEET_JSON, 'w', encoding='utf-8') as f:
        json.dump(sheets, f, indent=2, ensure_ascii=False)

def refresh_sheet(path, name):
    ly = os.path.join(path, f'{name}.ly')
    pdf = os.path.join(path, f'{name}.pdf')
    mid = os.path.join(path, f'{name}.mid')

    # Skip if files are up to date
    if not need_refresh(ly, pdf, mid):
        print(f'Skipped {name} (files are up to date)')
        return

    # Remove existing files
    if os.path.exists(pdf):
        os.remove(pdf)
    if os.path.exists(mid):
        os.remove(mid)

    # Generate new files
    command = f'{LILYPOND_PATH} -s -o "{path}" "{ly}"'
    subprocess.run(command, shell=True)

    print(f'Refreshed {name}')

def need_refresh(ly_path, pdf_path, mid_path):
    ly_mtime = os.path.getmtime(ly_path)
    
    # Check if .pdf or .mid files exist and are older than .ly
    for file_path in [pdf_path, mid_path]:
        if not os.path.exists(file_path):
            return True
        
        file_mtime = os.path.getmtime(file_path)
        if ly_mtime > file_mtime:
            return True
    
    return False

if __name__ == '__main__':
    refresh()
