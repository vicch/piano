"""music2ly shared library: MusicXML chunking and LLM MusicXML->LilyPond translation.

Common building blocks reused by the video2ly (audio) and image2ly (sheet image)
tools. Tool-specific input stages live in their own packages; this package owns
the source-agnostic MusicXML and LilyPond machinery plus configuration.
"""

__version__ = "0.1.0"
