\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn f''8.[ f''16] e''4 c''4 d''4 c''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
