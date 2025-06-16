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
    
    \cadenzaOn a''4. d''8 e''8[ fs''8 g''8 a''8] b''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}