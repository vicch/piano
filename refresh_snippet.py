"""
This script iterates all folders under current path, and for each ".ly" file, remove its associated PDF and MIDI files,
and execute LilyPond command to re-generate them.
"""
import os
import subprocess
import json

from pydub import AudioSegment

LILYPOND_PATH = 'D:/Programs/lilypond-2.24.3/bin/lilypond.exe'
FLUIDSYNTH_PATH = 'D:/Programs/fluidsynth-2.4.6/bin/fluidsynth.exe'
SOUNDFONT_PATH = 'D:/Piano/Steinway_Model_D274.sf2'

def refresh():
    root_dir = os.path.join(os.getcwd(), 'snippet')
    processed_files = []

    for _, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.ly'):
                refresh_file(root_dir, file)

                # Extract filename without extension
                name = os.path.splitext(file)[0]
                processed_files.append({
                    'name': name,
                    'png': f'snippet/{name}.png',
                    'mp3': f'snippet/{name}.mp3'
                })

    # Generate snippet.json
    json_path = os.path.join(os.getcwd(), 'snippet.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(processed_files, f, indent=2, ensure_ascii=False)

def refresh_file(dir, file):
    name = os.path.splitext(file)[0]

    pdf = os.path.join(dir, f'{name}.pdf')
    mid = os.path.join(dir, f'{name}.mid')
    wav = os.path.join(dir, f'{name}.wav')
    mp3 = os.path.join(dir, f'{name}.mp3')
    png = os.path.join(dir, f'{name}.png')
    cropped_png = os.path.join(dir, f'{name}.cropped.png')

    # Remove all existing files before generating new ones
    os.path.exists(pdf) and os.remove(pdf)
    os.path.exists(mid) and os.remove(mid)
    os.path.exists(wav) and os.remove(wav)
    os.path.exists(mp3) and os.remove(mp3)
    os.path.exists(png) and os.remove(png)
    os.path.exists(cropped_png) and os.remove(cropped_png)

    # Generate MIDI, PNG and cropped PNG
    command = f'{LILYPOND_PATH} -fpng -dresolution=500 -dcrop -s -o "{dir}" "{os.path.join(dir, file)}"'
    subprocess.run(command, shell=True)

    # Generate WAV from MIDI
    command = f'{FLUIDSYNTH_PATH} -q -n -i -r 44100 -F "{wav}" "{SOUNDFONT_PATH}" "{mid}"'
    subprocess.run(command, shell=True)

    # Generate MP3 from WAV
    audio = AudioSegment.from_wav(wav)
    audio.export(mp3, format='mp3')
    os.remove(wav)

    # Overwrite the full PNG with the cropped PNG
    if os.path.exists(png) and os.path.exists(cropped_png):
        os.remove(png)
        os.rename(cropped_png, png)

    print(f'Refreshed {name}')

if __name__ == '__main__':
    refresh()