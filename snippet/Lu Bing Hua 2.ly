\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 60
    \clef treble
    \key c \major
    
    \cadenzaOn g'16[ e'16] d'8.[ e'16] d'8[ d'8] b16[ a16 g16 b16] a4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
