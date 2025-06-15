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
    
    \cadenzaOn g'4 c''8[ a'8] g'4 g'4 e'8[ g'8 a'8 c''8] g'4 g'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}