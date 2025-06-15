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
    
    \cadenzaOn e'8[ g'8 c''8 a'8] g'2 e'8[ g'8 a'8 c''8] g'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}