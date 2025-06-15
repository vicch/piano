"""
1. Reads snippet config from snippet.json
2. For each snippet, generate the ./snippet/name.ly file based on template_snippet.ly
3. Generate the PNG and MP3 files via LilyPond and FluidSynth commands
4. Clean up intermediate files
"""

import os
import json

def refresh():
  for snippet in read_snippets():
    refresh_snippet(snippet)

def read_snippets():
  with open('snippet.json', 'r') as f:
    snippets = json.load(f)
  return snippets

def refresh_snippet(snippet):
  generate_ly(snippet)

def generate_ly(snippet):
  with open('template_snippet.ly', 'r') as f:
    template = f.read()

  template = template.replace('{name}', snippet['name'])
  template = template.replace('{tempo}', snippet['tempo'])
  template = template.replace('{key}', snippet['key'])

  for i, snippet_part in enumerate(snippet['snippets']):
    # Make a copy of the template
    template_copy = template
    template_copy = template_copy.replace('{snippet}', snippet_part)
    with open(f'./snippet/{snippet["name"]} {i+1}.ly', 'w') as f:
      f.write(template_copy)

if __name__ == '__main__':
  refresh()
