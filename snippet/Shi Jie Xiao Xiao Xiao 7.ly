\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn e''4. e''8 g''4 e''4 f''4. f''8 f''4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
