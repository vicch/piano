\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f
    
    \cadenzaOn d'4 g'4 e'8 c'4. \cadenzaOff
  }
  \layout {}
  \midi {}
}