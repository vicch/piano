\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 60
    \clef treble
    \key c \major
    
    \cadenzaOn e'8[ a16 d'16~] d'4. a16[ b16] c'8[ b8 c'8 d'8] d'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
