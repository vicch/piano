\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn b4 b8[ b8] b8[ d'8 c'8 b8] a4 a4 a2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
