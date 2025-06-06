\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Passacaglia"
  tagline = "Bilibili 471148656718506228"
  transcriber = "Transcribed by vicch"
}

\paper {
  total-page = 1
  scoreTitleMarkup = \markup \fill-line {
    \null { \fromproperty #'header:transcriber }
  }
}

\markup \vspace #1.5

CI  = { c,4 g,4 e2  }
DmI = { d,4 a,4 f2  }
EI  = { e,4 b,4 gs2 }
FI  = { f,4 c4  a2  }
GI  = { g,4 d4  b2  }
AmI = { a,4 e4  c'2 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      <a c' e' a'>2 a2 | <d' f' a'>2 a2 | <b d' g'>2 g2 | <c' e' g'>2 g2 | <a c' f'>2 f2 | <b d' f'>2 f2 | <gs b e'>2 e2 | gs2 b2 | \break
      
      c''8 c'''8 b''8 c'''8 a''8 c'''8 g''8 c'''8 | f''8 c'''8 e''8 c'''8 d''8 c'''8 c''8 c'''8 | b'8 b''8 a''8  b''8  g''8 b''8 f''8 b''8 | e''8 b''8 d''8 b''8 c''8 b''8 b'8 b''8 | \break
      a'8  a''8  g''8 a''8  f''8 a''8  e''8 a''8  | d''8 a''8  c''8 a''8  b'8  a''8  a'8  a''8  | a''4     gs''8 fs''8 gs''4.         a''8 | a''1                                   | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      <a,, a,>1 | <d, d>1 | <g,, g,>1 | <c, c>1 | <f,, f,>1 | <b,, b,>1 | e,1~ | e,1 |
      
      \AmI | \DmI | \GI | \CI  |
      \FI  | \DmI | \EI | \AmI |
    }
    \chords {
      
      a1 | d1 | g1 | c1 | f1 | b1 | e1 | e1 |
      
      a1:m | d1:m | g1 | c1   |
      f1   | d1:m | e1 | a1:m |
    }
  >>
  \layout {}
  \midi {}
}
