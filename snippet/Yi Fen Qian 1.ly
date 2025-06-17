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
    
    \cadenzaOn g'4 c''4 a'8[ c''8] g'4 e'8[ g'8 d'8 e'8] g'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}