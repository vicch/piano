\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

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