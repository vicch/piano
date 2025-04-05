\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "水晶"
  tagline = "EveryonePiano 313"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

Ci   = { c8  g8  c'8 e'8 g'4 }
Cii  = { c8  g8  c'8 d'8 e'4 }
Di   = { d,8 a,8 d8  fs8 a4  }
Emi  = { e,8 b,8 e8  g8  b4  }
Emii = { b,8 g8  b8  e'8 g'4 }
Fi   = { f,8 c8  f8  a8  c'4 }
Fii  = { f,8 c8  f8  g8  a4  }
Gi   = { g,8 d8  g8  b8  d'4 }
Gii  = { b,8 d8  g8  b8  d'4 }
Giii = { g,8 d8  g8  a8  b4  }
Ami  = { a,8 e8  a8  c'8 e'4 }

Dii   = { d,8 a,8 f2  }
Emiii = { e,8 b,8 g2  }
Fiii  = { f,8 c8  a2  }
Giv   = { g,8 d8  b2  }
Amii  = { a,8 e8  c'2 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      c''8 d''8 e''8 d''8 c''4 | d''4 g''2      | c''8 d''8 e''8 d''8 c''4 | b'4 g'2 | \break
      a'8  b'8  c''8 b'8  a'4  | g'4  c''4 e''4 | f''4      e''4      d''4 | c''2.   | \break
      
      e''4 d''4 c''4 | b'4  g''2       | f''4 g''4 a''4      | g''2. | \break
      f''4 g''4 a''4 | g''4 e''4. e''8 | f''4 e''4 d''8 c''8 | d''2. | \break
      e''4 d''4 c''4 | b'4  g''2       | f''4 g''4 a''4      | g''2. | \break
      f''4 g''4 a''4 | g''4 e''4. e''8 | f''4 e''4 d''4      | c''2. | \break
      
      a''2      b''8 c'''8 | b''2      e''8 f''8 | g''2 e''8 d''8 | c''2 r8 c''8 | \break
      f''4 e''4 f''4       | a''4 g''4 f''4      | g''2.(         | g''2.)       | \break 
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \Ci | \Gii | \Ami | \Emi |
      \Fi | \Ci  | \Gi  | \Ci  |
      
      \Ci  | \Emi | \Fi   | \Gi   |
      \Fi  | \Ci  | \Di   | \Gi   |
      \Cii | \Emi | \Fii  | \Giii |
      \Fii | \Cii | \Giii | \Cii  |
      
      \Fiii | \Giv | \Emiii | \Amii |
      \Dii  | \Giv | \Cii   | \Emii |
    }
    \chords {

      c2. | g2. | a2.:m | e2.:m |
      f2. | c2. | g2.   | c2.   |
      
      c2. | e2.:m | f2. | g2. |
      f2. | c2.   | d2. | g2. |
      c2. | e2.:m | f2. | g2. |
      f2. | c2.   | g2. | c2. |
      
      f2. | g2. | e2.:m | a2.:m |
      d2. | g2. | c2.   | e2.:m |
    }
  >>
  \layout {}
}

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      c''8 d''8 e''8 d''8 c''4 | d''4 g''2      | c''8 d''8 e''8 d''8 c''4 | b'4 g'2 | \break
      a'8  b'8  c''8 b'8  a'4  | g'4  c''4 e''4 | f''4      e''4      d''4 | c''2.   | \break
      
      e''4 d''4 c''4 | b'4  g''2       | f''4 g''4 a''4      | g''2. | \break
      f''4 g''4 a''4 | g''4 e''4. e''8 | f''4 e''4 d''8 c''8 | d''2. | \break
      e''4 d''4 c''4 | b'4  g''2       | f''4 g''4 a''4      | g''2. | \break
      f''4 g''4 a''4 | g''4 e''4. e''8 | f''4 e''4 d''4      | c''2. | \break
      
      a''2      b''8 c'''8 | b''2      e''8 f''8 | g''2 e''8 f''8 | c''2 r8 c''8 | \break
      f''4 e''4 f''4       | a''4 g''4 f''4      | g''2.(         | g''2.)       | \break 
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \Ci | \Gii | \Ami | \Emi |
      \Fi | \Ci  | \Gi  | \Ci  |
      
      \Ci  | \Emi | \Fi   | \Gi   |
      \Fi  | \Ci  | \Di   | \Gi   |
      \Cii | \Emi | \Fii  | \Giii |
      \Fii | \Cii | \Giii | \Cii  |
      
      \Fiii | \Giv | \Emiii | \Amii |
      \Dii  | \Giv | \Cii   | \Emii |
    }
  >>
  \midi {}
}
