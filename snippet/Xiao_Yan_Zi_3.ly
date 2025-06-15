\version "2.24.3"
\include "../settings.v1.ly"

\paper {
  total-page = 1
}

\score {
  \new Staff {
    \tempo 4 = 96
    \clef treble
    \key c \major
    
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f
    
    \cadenzaOn e'4. g'8 a'4 g'8[ a'8] c''4 d''8[ g'8] a'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}