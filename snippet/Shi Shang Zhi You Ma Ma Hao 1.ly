\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn a''4. g''8 e''4 g''4 c'''4 a''8[ g''8] a''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
