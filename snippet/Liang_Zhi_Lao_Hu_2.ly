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
    
    \cadenzaOn g'16[ a'16 g'16 f'16] e'8[ c'8] c'8[ g8] c'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}