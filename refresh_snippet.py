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
SOUNDFONT_PATH = 'D:/Piano/Clean Grand Mistral.sf2'

FILE_EXTENSIONS = {
  'pdf': '.pdf',
  'mid': '.mid',
  'wav': '.wav',
  'mp3': '.mp3',
  'png': '.png',
  'cropped_png': '.cropped.png'
}

def refresh():
  for snippet in read_snippets():
    # If the snippet's .ly file is already in the dir, skip it.
    if os.path.exists(os.path.join(SNIPPET_DIR, f'{snippet["name"]} 1.ly')):
      continue
    refresh_snippet(snippet)

def read_snippets():
  with open(SNIPPET_CONFIG, 'r') as f:
    snippets = json.load(f)
  return snippets

def refresh_snippet(snippet):
  file_names = generate_lys(snippet)
  for file_name in file_names:
    generate_files(file_name)

def generate_lys(snippet):
  names = []

  with open(SNIPPET_TEMPLATE, 'r') as f:
    template = f.read()

  template = template.replace('{name}', snippet['name'])
  template = template.replace('{tempo}', snippet['tempo'])
  template = template.replace('{key}', snippet['key'])

  # Each snippet part in "snippets" list generates its own .ly and other files
  for i, snippet_part in enumerate(snippet['snippets']):
    snippet_content = template
    snippet_content = snippet_content.replace('{snippet}', snippet_part)

    file_name = f'{snippet["name"]} {i+1}'
    file_path = os.path.join(SNIPPET_DIR, f'{file_name}.ly')
    with open(file_path, 'w') as f:
      f.write(snippet_content)

    names.append(file_name)

  return names

def generate_files(name):
  # The list of files related to the snippet
  files = {ext: os.path.join(SNIPPET_DIR, f'{name}{FILE_EXTENSIONS[ext]}') for ext in FILE_EXTENSIONS}

  # Remove all existing files before generating new ones
  for file in files.values():
    os.path.exists(file) and os.remove(file)

  # Generate MIDI, PNG and cropped PNG
  command = f'{LILYPOND_PATH} -fpng -dresolution=500 -dcrop -s -o "{SNIPPET_DIR}" "{os.path.join(SNIPPET_DIR, name)}"'
  subprocess.run(command, shell=True)

  # Generate WAV from MIDI
  command = f'{FLUIDSYNTH_PATH} -q -n -i -r 44100 -F "{files["wav"]}" "{SOUNDFONT_PATH}" "{files["mid"]}"'
  subprocess.run(command, shell=True)

  # Generate MP3 from WAV
  audio = AudioSegment.from_wav(files['wav'])
  audio.export(files['mp3'], format='mp3', bitrate="128k")
  os.remove(files['wav'])

  # Overwrite the full PNG with the cropped PNG
  if os.path.exists(files['png']) and os.path.exists(files['cropped_png']):
    os.remove(files['png'])
    os.rename(files['cropped_png'], files['png'])

  print(f'Refreshed {name}')

if __name__ == '__main__':
  refresh()
