\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Canon"
  tagline = "EveryonePiano 8499"
}

\paper {
  total-page = 2
}

\markup \vspace #1.5

Ci   = { c4  e4  g2  }
Cii  = { c'4 e'4 g'2 }
Ciii = { c4  g4  e'2 }
Civ  = { c,4 g,4 e2  }
Emi  = { e4  g4  b2  }
Emii = { e,4 b,4 g2  }
Fi   = { f4  a4  c'2 }
Fii  = { f,4 c4  a2  }
Gi   = { g4  b4  d'2 }
Gii  = { g,4 d4  b2  }
Ami  = { a4  c'4 e'2 }
Amii = { a,4 e4  c'2 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 4/4
      
      e''1^5 | d''1  | c''1  | b'1 | \break
      a'1    | g'1^3 | a'1^1 | b'1 | \break
      
      e''2^4 e''4 c''4 | d''2. b'4 | c''2^4 c''4 a'4  | b'2.      g'4  | \break
      a'2^4  a'4  f'4  | g'2.  e'4 | a'2^2  a'4  c''4 | b'2  c''4 d''4 | \break
      
      e''4^2 d''4 e''4   f''4 | g''4  d''4 g''4 f''4   | e''4   a''4 g''4 f''4 | g''4 f''4 e''4 d''4 | \break
      c''4^2 a'4  a''4^3 b''4 | c'''4 b''4 a''4 g''4^1 | f''4^3 e''4 d''4 a''4 | g''4 a''4 g''4 f''4 | \break
      
      g''4^5 e''8 f''8 g''4 e''8  f''8 | g''8  g'8^1 a'8 b'8    c''8^1 d''8  e''8 f''8 |
      e''4^5 c''8 d''8 e''4 e'8^1 f'8  | g'8   a'8   g'8 f'8    g'8    e'8   f'8  g'8  | \break
      f'4    a'8  g'8  f'4  e'8^3 d'8  | e'8   d'8   c'8 d'8    e'8    f'8^1 g'8  a'8  |
      f'4    a'8  g'8  a'4  b'8   c''8 | g'8^1 a'8   b'8 c''8^1 d''8   e''8  f''8 g''8 | \break
      
      g''2.^4 g''4   | g''4 a''4 g''4 f''4 | e''2. e''4^4 | e''4 f''4 e''4 d''4 | \break
      c''2.   c''4^3 | c''4 d''4 c''4 bf'4 | a'2.  c''4   | b'2       c''4 d''4 | \break
      
      e''1^5 | d''1 | c''1 | b'1 | \break

      a'1 | g'1^3 | a'2. c''4 | b'8 c''8 b'8 c''8 \tuplet 3/2 { b'8 c''8 b'8 } a'8 b'8 | c''1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \Cii | \Gi | \Ami | \Emi |
      \Fi  | \Ci | \Fi  | \Gi  |
      
      \Cii | \Gi | \Ami | \Emi |
      \Fi  | \Ci | \Fi  | \Gi  |
      
      \Ciii | \Gii | \Amii | \Emii |
      \Fii  | \Civ | \Fii  | \Gii  |
      
      \Ciii | \Gii | \Amii | \Emii |
      \Fii  | \Civ | \Fii  | \Gii  |
      
      \Ciii | \Gii | \Amii | \Emii |
      \Fii  | \Civ | \Fii  | \Gii  |
      
      \Cii | \Gi | \Ami | \Emi |
      \Fi  | \Ci | \Fi  | \Gi  | <c' e'>1 |
    }
    \chords {
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | f1   | g1   |
      
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | f1   | g1   |
      
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | f1   | g1   |
      
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | f1   | g1   |
      
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | f1   | g1   |
      
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | f1   | g1   | r1 |
    }
  >>
  \layout {}
  \midi {}
}
