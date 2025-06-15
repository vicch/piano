\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Passacaglia"
  tagline = "YouTube M3uD6vPIKEA"
  transcriber = "Transcribed by vicch"
}

\paper {
  total-page = 1
  scoreTitleMarkup = \markup \fill-line {
    \null { \fromproperty #'header:transcriber }
  }
}

\markup \vspace #1.5

CI  = { c,4 g,4 e4  r4 }
DmI = { d,4 a,4 f4  r4 }
EI  = { e,4 b,4 gs4 r4 }
FI  = { f,4 c4  a4  r4 }
GI  = { g,4 d4  b4  r4 }
AmI = { a,4 e4  c'4 r4 }

CII  = { c,4 g,4 e4  g,4 }
DmII = { d,4 a,4 f4  a,4 }
EII  = { e,4 b,4 gs4 b,4 }
FII  = { f,4 c4  a4  c4  } 
GII  = { g,4 d4  b4  d4  }

CIII  = { c,8 g,8 c8 d8 e8  r4. }
DmIII = { d,8 a,8 d8 e8 f8  r4. }
FIII  = { f,8 c8  f8 g8 a8  r4. }
GIII  = { g,8 d8  g8 a8 b8  r4. }
AmIII = { a,8 e8  a8 b8 c'8 r4. }

CIV  = { c,4 g,4 <e g>4  r4 }
DmIV = { d,4 a,4 <f a>4  r4 }
FIV  = { f,4 c4  <f a>4  r4 }
GIV  = { g,4 d4  <g b>4  r4 }
AmIV = { a,4 e4  <a c'>4 r4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      \clef "treble_8"
      << { <c' e' a'>1 } \\ { a2 a2 } >> | << { <d' f' a'>1 } \\ { s2 a2 } >> | << { <b d' g'>1 } \\ { s2 g2 } >> | << { <c' e' g'>1 } \\ { s2 g2 } >> | << { <a c' f'>1 } \\ { s2 f2 } >> | << { <b d' f'>1 } \\ { s2 f2 } >> | <gs b e'>2 e2 | gs2 b2 | \break
      
      \A \clef treble
      c''8 c'''8 b''8 c'''8 a''8 c'''8 g''8 c'''8 | f''8 c'''8 e''8 c'''8 d''8 c'''8 c''8 c'''8 | b'8 b''8 a''8  b''8  g''8 b''8 f''8 b''8 | e''8 b''8 d''8 b''8 c''8 b''8 b'8 b''8 | \break
      a'8  a''8  g''8 a''8  f''8 a''8  e''8 a''8  | d''8 a''8  c''8 a''8  b'8  a''8  a'8  a''8  | a''4     gs''8 fs''8 gs''4.         a''8 | a''1                                   | \break
      
      c'''8 c''8 d''8 c''8 e''8 c''8 f''8 c''8 | g''8 c''8 a''8 c''8 b''8 c''8 c'''8 c''8 | b''8 b'8 c''8  b'8   d''8 b'8 e''8 b'8  | f''8 b'8 g''8 b'8 a''8 b'8 b''8 b'8 | \break
      a''8  a'8  b'8  a'8  c''8 a'8  d''8 a'8  | e''8 a'8  f''8 a'8  g''8 a'8  a''8  a'8  | a''4     gs''8 fs''8 gs''4.        a''8 | a''1                                | \break
      
      c''8 c'''8 b''8 c'''8 a''8 c'''8 g''8 c'''8 | f''8 c'''8 e''8 c'''8 d''8 c'''8 c''8 c'''8 | b'8 b''8 a''8  b''8  g''8 b''8 f''8 b''8 | e''8 b''8 d''8 b''8 c''8 b''8 b'8 b''8 | \break
      a'8  a''8  g''8 a''8  f''8 a''8  e''8 a''8  | d''8 a''8  c''8 a''8  b'8  a''8  a'8  a''8  | a''4     gs''8 fs''8 gs''4.         a''8 | a''1                                   | \break
      
      c'''8 c''8 d''8 c''8 e''8 c''8 f''8 c''8 | g''8 c''8 a''8 c''8 b''8 c''8 c'''8 c''8 | b''8 b'8 c''8  b'8   d''8 b'8 e''8 b'8  | f''8 b'8 g''8 b'8 a''8 b'8 b''8 b'8 | \break
      a''8  a'8  b'8  a'8  c''8 a'8  d''8 a'8  | e''8 a'8  f''8 a'8  g''8 a'8  a''8  a'8  | a''4     gs''8 fs''8 gs''4.        a''8 | a''1                                | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \clef "bass_8"
      <a,, a,>1 | <d, d>1 | <g,, g,>1 | <c, c>1 | <f,, f,>1 | <b,, b,>1 | e,1~ | e,1 |
      
      \clef bass
      \AmI | \DmI | \GI | \CI  |
      \FI  | \DmI | \EI | \AmI |
      
      \AmI | \DmI  | \GII | \CII |
      \FII | \DmII | \EII | \AmI |
      
      \AmIII | \DmIII | \GIII | \CIII |
      \FIII  | \DmIII | \EI   | \AmI  |
      
      \AmIV | \DmIV | \GIV | \CIV |
      \FIV  | \DmIV | \EI  | \AmI |
    }
    \chords {
      
      a1 | d1 | g1 | c1 | f1 | b1 | e1 | e1 |
      
      a1:m | d1:m | g1 | c1   |
      f1   | d1:m | e1 | a1:m |
      
      a1:m | d1:m | g1 | c1   |
      f1   | d1:m | e1 | a1:m |
      
      a1:m | d1:m | g1 | c1   |
      f1   | d1:m | e1 | a1:m |
      
      a1:m | d1:m | g1 | c1   |
      f1   | d1:m | e1 | a1:m |
    }
  >>
  \layout {}
  \midi {}
}
