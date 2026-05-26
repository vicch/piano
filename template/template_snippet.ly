\version "2.24.3"
\include "../template/base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = {tempo}
    \clef treble
    \key {key}
    
    \cadenzaOn {snippet} \cadenzaOff
  }
  \layout {}
  \midi {}
}
