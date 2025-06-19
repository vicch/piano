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
    
    \cadenzaOn c''4 a''4 a''8[ bf''8 a''8 g''8] f''4 d''4 \cadenzaOff
  }
  \layout {}
  \midi {}
}