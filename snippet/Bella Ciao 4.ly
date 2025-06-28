\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn d''8[ c''8] b'4 e''4 b'4 c''4 a'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
