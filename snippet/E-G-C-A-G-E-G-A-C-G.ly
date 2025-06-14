\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \clef treble
    \key c \major
    \override Staff.TimeSignature.stencil = ##f
    
    \cadenzaOn e'8[ g'8 c''8 a'8] g'2 e'8[ g'8 a'8 c''8] g'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}