\version "2.24.3"
\include "../template/base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn f'4 d'4 f'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
