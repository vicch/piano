\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn g'8[ a'8 g'8 a'8] g'8[ a'8] g'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
