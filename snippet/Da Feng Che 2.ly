\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn d'8 d'4 c'8 d'8 d'4 c'8 c''4. a'8 g'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}
