\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn a'4 g'8[ e'8] d'4 d'4 e'8[ g'8 e'8 d'8] c'4 c'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
