\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn a'8[ a'8] c''4 g'8[ a'8] e'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
