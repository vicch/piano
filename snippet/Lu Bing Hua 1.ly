\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 60
    \clef treble
    \key c \major
    
    \cadenzaOn a'8.[ a'16] c''8[ a'8] g'16[ g'8] e'16[ g'8] \cadenzaOff
  }
  \layout {}
  \midi {}
}
