\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn f''4. g''8 a''8[ a''8 g''8 f''8] a''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}