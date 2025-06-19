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
    
    \cadenzaOn g'8[ g'8 g'8 a'8] c''4 c''8[ d''8] f'4. d'8 f'2 \cadenzaOff
  }
  \layout {}
  \midi {}
}