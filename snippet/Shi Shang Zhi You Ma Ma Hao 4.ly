\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn g''4. e''8 d''8[ c''8 a'8 c''8] g'1 \cadenzaOff
  }
  \layout {}
  \midi {}
}
