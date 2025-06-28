\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn g''4. c''8 d''8[ e''8 f''8 g''8] a''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
