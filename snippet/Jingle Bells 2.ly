\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn a'8 a'8[ f''8 e''8 d''8] b'4 r8 b'8 g''8[ g''8 f''8 d''8] e''4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
