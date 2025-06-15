"""
1. Reads snippet config from snippet.json
2. For each snippet, generate the ./snippet/name.ly file based on template_snippet.ly
3. Generate the PNG and MP3 files via LilyPond and FluidSynth commands
4. Clean up intermediate files
"""

import os
import json
import subprocess

from pydub import AudioSegment

SNIPPET_CONFIG = 'snippet.json'
SNIPPET_TEMPLATE = 'template_snippet.ly'
SNIPPET_DIR = 'snippet'

LILYPOND_PATH = 'D:/Programs/lilypond-2.24.3/bin/lilypond.exe'
FLUIDSYNTH_PATH = 'D:/Programs/fluidsynth-2.4.6/bin/fluidsynth.exe'
SOUNDFONT_PATH = 'D:/Piano/Steinway_Model_D274.sf2'

def refresh():
  for snippet in read_snippets():
    refresh_snippet(snippet)

def read_snippets():
  with open(SNIPPET_CONFIG, 'r') as f:
    snippets = json.load(f)
  return snippets

def refresh_snippet(snippet):
  generate_ly(snippet)
  generate_files(snippet)

def generate_ly(snippet):
  with open(SNIPPET_TEMPLATE, 'r') as f:
    template = f.read()

  template = template.replace('{name}', snippet['name'])
  template = template.replace('{tempo}', snippet['tempo'])
  template = template.replace('{key}', snippet['key'])

  for i, snippet_part in enumerate(snippet['snippets']):
    # Make a copy of the template
    template_copy = template
    template_copy = template_copy.replace('{snippet}', snippet_part)

    file_path = os.path.join(SNIPPET_DIR, f'{snippet["name"]} {i+1}.ly')
    with open(file_path, 'w') as f:
      f.write(template_copy)

def generate_files(snippet):
  name = snippet['name']

  pdf = os.path.join(SNIPPET_DIR, f'{name}.pdf')
  mid = os.path.join(SNIPPET_DIR, f'{name}.mid')
  wav = os.path.join(SNIPPET_DIR, f'{name}.wav')
  mp3 = os.path.join(SNIPPET_DIR, f'{name}.mp3')
  png = os.path.join(SNIPPET_DIR, f'{name}.png')
  cropped_png = os.path.join(SNIPPET_DIR, f'{name}.cropped.png')

  # Remove all existing files before generating new ones
  os.path.exists(pdf) and os.remove(pdf)
  os.path.exists(mid) and os.remove(mid)
  os.path.exists(wav) and os.remove(wav)
  os.path.exists(mp3) and os.remove(mp3)
  os.path.exists(png) and os.remove(png)
  os.path.exists(cropped_png) and os.remove(cropped_png)

  # Generate MIDI, PNG and cropped PNG
  command = f'{LILYPOND_PATH} -fpng -dresolution=500 -dcrop -s -o "{SNIPPET_DIR}" "{os.path.join(SNIPPET_DIR, name)}"'
  subprocess.run(command, shell=True)

  # Generate WAV from MIDI
  command = f'{FLUIDSYNTH_PATH} -q -n -i -r 44100 -F "{wav}" "{SOUNDFONT_PATH}" "{mid}"'
  subprocess.run(command, shell=True)

  # Generate MP3 from WAV
  audio = AudioSegment.from_wav(wav)
  audio.export(mp3, format='mp3' bitrate="128k")
  os.remove(wav)

  # Overwrite the full PNG with the cropped PNG
  if os.path.exists(png) and os.path.exists(cropped_png):
      os.remove(png)
      os.rename(cropped_png, png)

  print(f'Refreshed {name}')

if __name__ == '__main__':
  refresh()
