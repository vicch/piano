\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f
    
    \cadenzaOn e''8[ g''8 e''8 d''8] c''2 d''8[ d''8 e''8 d''8] c''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}