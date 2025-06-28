\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn d''4 g''4 g''8[ a''8 g''8 f''8] e''4 c''4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
