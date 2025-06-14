\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \clef treble
    \key c \major
    \override Staff.TimeSignature.stencil = ##f
    
    \cadenzaOn \cadenzaOff
  }
  \layout {}
  \midi {}
}