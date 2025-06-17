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
    
    \cadenzaOn d''8[ d''8 d''8 e''8] g''8[ g''8] r8 g'8 a'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}