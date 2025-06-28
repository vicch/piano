\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 72
    \clef treble
    \key c \major
    
    \cadenzaOn g'4 c''4 c''8[ c''8] c''4 e''4 g''4 e''4 c''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
