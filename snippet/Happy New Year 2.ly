\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn c''8[ e''8] g''4 g''4 f''8[ e''8] d''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
