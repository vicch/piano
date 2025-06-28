\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn d'8[ d'8 d'8 e'8] c'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
