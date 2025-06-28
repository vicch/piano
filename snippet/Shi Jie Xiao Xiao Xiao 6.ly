\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn d''4. d''8 f''4 d''4 e''4. e''8 e''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
