\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Kiss the Rain"
  tagline = "Sequence"
  transcriber = "Transcribed by vicch"
}

\paper {
  total-page = 1
  scoreTitleMarkup = \markup \fill-line {
    \null { \fromproperty #'header:transcriber }
  }
}

\markup \vspace #1.5

CI  = { c8  g8  c'8 d'8 e'8 r8 }
DmI = { d8  a8  d'8 e'8 f'8 r8 }
EmI = { e,8 b,8 e8  g8  b8  r8 }
FI  = { f,8 c8  f8  g8  a8  r8 }
GI  = { g,8 d8  g8  a8  b8  r8 }
AmI = { a,8 e8  a8  b8  c'8 r8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 72
      \clef treble
      \key c \major
      \time 4/4
      
      \partial 4    r16   a'16 c''16 d''16 | d''8 e''8 e''2 r16 c''16 d''16 e''16 | d''8 g''8 g''2 r16 g''16 a''16 b''16 | b''8 c'''8 c'''4. d'''8 \tuplet 3/2 { e''' d''' c'''} | \break
      b''2 r8 c'''8 b''8       g''8        | g''8 a''8 a''2 r8        g''16 f''16 | e''8 g''8 g''2 c''8      d''8        | e''8 f''8  f''2         g''8 f''8                     | \break
      e''2.         d''16 a'16 c''16 d''16 |
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
           r4        | \CI r4 | \EmI r4 | \AmI r4 |
      \GI  r4        | \FI r4 | \CI  r4 | \DmI r4 |
      \EmI <g b d'>4 |
    }
    \chords {
      
            r4 | c2. r4 | e2.:m r4 | a2.:m r4 |
      g2.   r4 | f2. r4 | c2.   r4 | d2.:m r4 |
      e2.:m g4 |
    }
  >>
  \layout {}
  \midi {}
}
