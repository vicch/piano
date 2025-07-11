\version "2.24.3"

#(define title      "The End of the World")
#(define title-font "")
#(define sequence   "EveryonePiano 5556")
#(define total-page 2)

\include "../base.ly"

\markup \vspace #1.5

C      = { c8  g8  c'8 e'8  c'8 g8  }
Dm     = { d8  a8  d'8 f'8  d'8 a8  }
Em     = { e,8 b,8 e8  g8   e8  b,8 }
F      = { f,8 c8  f8  a8   f8  c8  }
G      = { g,8 d8  g8  b8   g8  d8  }
Gseven = { g,8 g8  b8  f'8  b8  g8  }
A      = { a,8 e8  a8  cs'8 a8  e8  }
Am     = { a,8 e8  a8  c'8  a8  e8  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 6/8
      
      \repeat volta 2 {
        e''2^3 e''8 d''8 | c''4. e''4^2 a''8 | g''8 d''4.~ d''4~ | d''4. r4. | \break
        c''2^3 c''8 b'8  | a'4.  c''4^2 f''8 | e''2.~            | e''4. r4. | \break
        
        d''4.^1 a''4^4 g''8 | a''2 g''8 a''8 | b''4. g''4 e''8 | g''4.~ g''4 e''8^2 | \break
        
        \alternative {
          \volta 1 {
            a''4. g''4. | f''8 e''4. d''8 e''8 | f''2.~ | f''4. r4. | \break
          }
          \volta 2 {
            a''4 f''8 d''4 c''8^3 | b'4. d''4. | c''2.~ | c''4. r4 c''8^2 | \bar "|." \break
          }
        }
      }
      
      a'4^1 a'8 c''4^2 c''8 | f''4^3 f''8 a''4 a''8 | g''8 e''4~ e''4.~ | e''4.  r4   c''8^2 | \break
      b'4   b'8 d''4^2 d''8 | f''4.^3     a''4 a''8 | g''2.~            | g''4.~ g''4 a''8^4 | \break
      
      b''4. g''4 e''8 | g''2       g''8 a''8 | b''4. g''4 e''8 | g''4.~ g''4 e''8^2 | \break
      a''4. g''4.     | f''8 e''4. d''8 e''8 | f''2.~          | f''4.  r4.         | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 6/8
      
      \C  | \C  | \G  | \G  |
      \Am | \Am | \Em | \Em |
      
      \Dm | \Dm | \Em     | \A      |
      
      \Dm | \Dm     | \Gseven | \Gseven |
      \Dm | \Gseven | \C      | \C      |
      
      \F | \F | \C | \C |
      \G | \G | \C | \C |
      
      \Em | \Em | \A      | \A      |
      \Dm | \Dm | \Gseven | \Gseven |
    }
    \chords {
      c2.   | c2.   | g2.   | g2.   |
      a2.:m | a2.:m | e2.:m | e2.:m |
      
      d2.:m | d2.:m | e2.:m | a2.   |
      
      d2.:m | d2.:m | g2.:7 | g2.:7 |
      d2.:m | g2.:7 | c2.   | c2.   |
      
      f2. | f2. | c2. | c2. |
      g2. | g2. | c2. | c2. |
      
      e2.:m | e2.:m | a2.   | a2.   |
      d2.:m | d2.:m | g2.:7 | g2.:7 |
    }
  >>
  \layout {}
  \midi {}
}
