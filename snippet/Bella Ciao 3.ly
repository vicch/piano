\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn d''8[ e''8] f''4 f''2 a''8 g''8[ f''8] a''8 e''2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
