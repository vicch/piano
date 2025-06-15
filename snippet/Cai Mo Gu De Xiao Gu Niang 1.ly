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
    
    \cadenzaOn a'4 e''4 e''4 e''4 e''8[ d''8] c''4 d''4 \cadenzaOff
  }
  \layout {}
  \midi {}
}