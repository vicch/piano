"""
This script iterates all folders under current path, and for each ".ly" file, remove its associated PDF and MIDI files,
and execute LilyPond command to re-generate them.
"""
import os
import subprocess

LILYPOND_PATH = 'D:/Programs/lilypond-2.24.3/bin/lilypond.exe'

EXCLUDES = ['structure.v1.ly', 'template.v1.ly']

def refresh():
    for root, dirs, files in os.walk(os.getcwd()):
        dirs[:] = [d for d in dirs if not d.startswith('.')]  # Skip dirs starting with "."
        for file in files:
            if file.endswith('.ly') and file not in EXCLUDES:
                refresh_file(root, file)

def refresh_file(folder, file):
    name = os.path.splitext(file)[0]
    pdf = os.path.join(folder, f'{name}.pdf')
    midi = os.path.join(folder, f'{name}.mid')
    if os.path.exists(pdf):
        os.remove(pdf)
    if os.path.exists(midi):
        os.remove(midi)

    command = f'{LILYPOND_PATH} -s -o "{folder}" "{os.path.join(folder, file)}"'
    subprocess.run(command, shell=True)

    print(f'Refreshed {name}')

if __name__ == '__main__':
    refresh()