\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn e'4 e'8[ g'8] g'4 g'4 a'4 a'8[ d''8] c''4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
