\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn d''4. e''8 g''4 g''8[ a''8] e''4 d''4 c''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}