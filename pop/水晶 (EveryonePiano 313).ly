\version "2.24.3"

#(define title      "水晶")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 313")
#(define total-page 3)

\include "../base.ly"

\markup \vspace #1.5

CI   = { c8  g8  c'8 e'8 g'4 }
CII  = { c8  g8  c'8 d'8 e'4 }
DI   = { d,8 a,8 d8  fs8 a4  }
EmI  = { e,8 b,8 e8  g8  b4  }
EmII = { b,8 g8  b8  e'8 g'4 }
FI   = { f,8 c8  f8  a8  c'4 }
FII  = { f,8 c8  f8  g8  a4  }
GI   = { g,8 d8  g8  b8  d'4 }
GII  = { b,8 d8  g8  b8  d'4 }
GIII = { g,8 d8  g8  a8  b4  }
AmI  = { a,8 e8  a8  c'8 e'4 }

Dm    = { d,8 a,8 f2  }
DII   = { d,8 a,8 fs2 }
EmIII = { e,8 b,8 g2  }
FIII  = { f,8 c8  a2  }
GIV   = { g,8 d8  b2  }
AmII  = { a,8 e8  c'2 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      c''8^1 d''8 e''8 d''8 c''4 | d''4 g''2          | c''8^3 d''8 e''8 d''8 c''4 | b'4 g'2 | \break
      a'8^2  b'8  c''8 b'8  a'4  | g'4  c''4^2 e''4^4 | f''4        e''4      d''4 | c''2.   | \break
      
      \A
      e''4^4 d''4 c''4 | b'4  g''2^4       | f''4   g''4 a''4      | g''2. | \break
      f''4   g''4 a''4 | g''4 e''4.^2 e''8 | f''4^4 e''4 d''8 c''8 | d''2. | \break
      e''4   d''4 c''4 | b'4  g''2         | f''4   g''4 a''4      | g''2. | \break
      f''4   g''4 a''4 | g''4 e''4.   e''8 | f''4   e''4 d''4      | c''2. | \break
      
      \B
      a''2^3           b''8 c'''8 | b''2      e''8^3 f''8 | g''2  e''8 d''8 | c''2 r8 c''8 | \break
      f''4^3      e''4 f''4       | a''4 g''4 f''4        | g''2.~          | g''2.        | \break
      a''2             b''8 c'''8 | b''2      e''8^1 f''8 | g''2  d'''4^5   | c'''2.       | \break
      f''8^2 e''8 f''4 g''4^1     | a''4 a''4 c'''4       | d'''2 b''8 a''8 | g''2.        | \break
      
      \C
      e''4^1 g''4^2 g''8 e''8 | a''4 g''2              | a''4   b''4 c'''4     | g''2.             | \break
      a''4   b''4   c'''4     | g''4 e''4  e''4        | f''4^4 e''4 d''8 c''8 | d''2.             | \break
      e''4   g''4   g''8 e''8 | a''4 g''4. g''8        | a''4^1 b''4 c'''4     | e'''2 e'''8 e'''8 | \break
      d'''4  c'''4.      a''8 | g''2       d''8^2 e''8 | d''4   c''2~          | c''2.             | c''2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \CI | \var \GII | \AmI | \EmI |
      \FI | \CI       | \GI  | \CI  |
      
      \CI  | \EmI | \FI   | \GI   |
      \FI  | \CI  | \DI   | \GI   |
      \CII | \EmI | \FII  | \GIII |
      \FII | \CII | \GIII | \CII  |
      
      \FIII | \GIV | \EmIII | \AmII |
      \Dm   | \GIV | \CII   | \EmII |
      \FIII | \GIV | \EmIII | \AmII |
      \FIII | \Dm  | \DII   | \GI   |
      
      \CI | \EmI | \FI  | \GI |
      \FI | \CI  | \DI  | \GI |
      \CI | \EmI | \EmI | \CI |
      \FI | \GI  | \CII | \CI | <c g c'>2. |
    }
    \chords {
      c2. | g2. | a2.:m | e2.:m |
      f2. | c2. | g2.   | c2.   |
      
      c2. | e2.:m | f2. | g2. |
      f2. | c2.   | d2. | g2. |
      c2. | e2.:m | f2. | g2. |
      f2. | c2.   | g2. | c2. |
      
      f2.   | g2.   | e2.:m | a2.:m |
      d2.:m | g2.   | c2.   | e2.:m |
      f2.   | g2.   | e2.:m | a2.:m |
      f2.   | d2.:m | d2.   | g2.   |
      
      c2. | e2.:m | f2.   | g2. |
      f2. | c2.   | d2.   | g2. |
      c2. | e2.:m | e2.:m | c2. |
      f2. | g2.   | c2.   | c2. | c2. |
    }
  >>
  \layout {}
  \midi {}
}
