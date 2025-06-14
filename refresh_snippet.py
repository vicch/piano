"""
This script iterates all folders under current path, and for each ".ly" file, remove its associated PDF and MIDI files,
and execute LilyPond command to re-generate them.
"""
import os
import subprocess

LILYPOND_PATH = 'D:/Programs/lilypond-2.24.3/bin/lilypond.exe'

def refresh():
    root_dir = os.path.join(os.getcwd(), 'snippet')
    for _, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.ly'):
                refresh_file(root_dir, file)

def refresh_file(dir, file):
    name = os.path.splitext(file)[0]

    pdf = os.path.join(dir, f'{name}.pdf')
    midi = os.path.join(dir, f'{name}.mid')
    png = os.path.join(dir, f'{name}.png')
    cropped_png = os.path.join(dir, f'{name}.cropped.png')

    if os.path.exists(pdf):
        os.remove(pdf)
    if os.path.exists(midi):
        os.remove(midi)
    if os.path.exists(png):
        os.remove(png)
    if os.path.exists(cropped_png):
        os.remove(cropped_png)

    command = f'{LILYPOND_PATH} -fpng -dresolution=300 -dcrop -s -o "{dir}" "{os.path.join(dir, file)}"'
    subprocess.run(command, shell=True)

    if os.path.exists(png) and os.path.exists(cropped_png):
        os.remove(png)
        os.rename(cropped_png, png)

    print(f'Refreshed {name}')

if __name__ == '__main__':
    refresh()