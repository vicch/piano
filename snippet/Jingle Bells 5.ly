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
    
    \cadenzaOn f''4 f''4 f''4 f''4 f''4 e''4 e''2 e''4 d''4 d''4 c''4 d''2 g''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}