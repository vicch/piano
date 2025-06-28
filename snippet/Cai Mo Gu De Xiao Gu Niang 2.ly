\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn d''4. c''8 d''4 c''4 d''8[ c''8 a'8 g'8] a'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
