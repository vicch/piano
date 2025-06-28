\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn g'16[ a'16 g'16 f'16] e'8[ c'8] c'8[ g8] c'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
