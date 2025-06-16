\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \cadenzaOn e'8 a'8[ b'8] c''4 b'8[ a'8] c''4 b'8[ a'8] e''4 e''4 e''4 \cadenzaOff
  }
  \layout {}
  \midi {}
}