\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn c''4. d''8 e''4. c''8 e''4 c''4 e''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
