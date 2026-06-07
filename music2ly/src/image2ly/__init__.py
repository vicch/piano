"""image2ly: sheet music image -> LilyPond via OMR.

Pipeline: image -> [OMR engine: homr/oemer] -> MusicXML -> chunk -> LLM translate
(reusing music2ly.lilypond) -> merged LilyPond score.
"""

__version__ = "0.1.0"
