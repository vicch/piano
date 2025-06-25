"""
This script iterates all folders under current path, and for each ".ly" file, remove its associated PDF and MIDI files,
and execute LilyPond command to re-generate them.
"""
import os
import subprocess
import json

LILYPOND_PATH = 'D:/Programs/lilypond-2.24.3/bin/lilypond.exe'

EXCLUDE_DIRS = ['snippet']
EXCLUDE_FILES = ['base.ly', 'template.ly', 'template_snippet.ly']

SHEET_JSON = 'sheet.json'

def refresh():
    sheets = {}
    
    for root, dirs, files in os.walk(os.getcwd()):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not d in EXCLUDE_DIRS]  # Skip dirs starting with "."
        for file in files:
            if file.endswith('.ly') and file not in EXCLUDE_FILES:
                refresh_sheet(root, file)
                if root not in sheets:
                    sheets[root] = []
                sheets[root].append(file)

    # Export the collected map to sheet.json
    with open(SHEET_JSON, 'w', encoding='utf-8') as f:
        json.dump(sheets, f, indent=2, ensure_ascii=False)

def refresh_sheet(category, sheet):
    name = os.path.splitext(sheet)[0]
    pdf = os.path.join(category, f'{name}.pdf')
    midi = os.path.join(category, f'{name}.mid')

    # Remove existing files
    if os.path.exists(pdf):
        os.remove(pdf)
    if os.path.exists(midi):
        os.remove(midi)

    # Generate new files
    command = f'{LILYPOND_PATH} -s -o "{category}" "{os.path.join(category, sheet)}"'
    subprocess.run(command, shell=True)

    print(f'Refreshed {name}')

if __name__ == '__main__':
    refresh()
