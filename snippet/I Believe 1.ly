\version "2.24.3"
\include "../base_snippet.ly"

\score {
  \new Staff {
    \set Score.tempoHideNote = ##t
    \override Staff.TimeSignature.stencil = ##f

    \tempo 4 = 60
    \clef treble
    \key c \major
    
    \cadenzaOn g'8[ c'16 d'16~] d'4. d'16[ e'16] f'8[ e'16 f'16~] f'16[ g'8 e'16~] e'4 \cadenzaOff
  }
  \layout {}
  \midi {}
}
