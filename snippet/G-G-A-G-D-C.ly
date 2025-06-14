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
    
    \cadenzaOn g'8.[ g'16] a'4 g'4 d''4 c''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}