\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 120
    \clef treble
    \key c \major
    
    \cadenzaOn d'8[ e'8] f'4 d''4 b'4 c''8[ b'8] a'4 g'4 g'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
