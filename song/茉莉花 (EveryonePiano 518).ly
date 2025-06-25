\version "2.24.3"

#(define title      "茉莉花")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 518")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

Cfive   = { c8  g8  c'8 g8  }
Dfive   = { d8  a8  d'8 a8  }
Dseven  = { d8  fs8 a8  c'8 }
Efive   = { e8  b8  e'8 b8  }
Ffivei  = { f8  c'8 f'8 c'8 }
Ffiveii = { f,8 c8  f8  c8  }
Gfivei  = { g8  d'8 g'8 d'8 }
Gfiveii = { g,8 d8  g8  d8  }
Afive   = { a,8 e8  a8  e8  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      e''4^1       e''8 g''8^2 a''8 c'''8 c'''8 a''8   | g''4   g''8 a''8  g''2         | e''4   e''8 g''8 a''8   c'''8 c'''8  a''8 | g''4 g''8 a''8 g''2                     | \break
      g''4^2       g''4        g''4       e''8  g''8   | a''4   a''4       g''2         | e''4^3 d''8 e''8 g''4         e''8   d''8 | c''4 c''8 d''8 c''2                     | \break
      e''8^3  d''8 c''8 e''8   d''4.            e''8^1 | g''4^2 a''8 c'''8 g''2         | d''4^2 e''8 g''8 d''8^3 e''8  c''8^3 a'8  | g'2            a'4^2 a'8  c''8^3        | \break
      d''4.             e''8   c''8 d''8  c''8  a'8    | g'2               a'4 a'8 c''8 | d''4.       e''8 c''8^2 d''8  c''8   a'8  | g''2^5         <b'' d''' g'''>2\arpeggio | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \Cfive   \Cfive   | \Cfive   \Cfive   | \Cfive   \Cfive  | \Cfive c8^5 g8^2 c8^5 d8^4   |
      \Efive   \Efive   | \Ffivei  \Gfivei  | \Cfive   \Cfive  | \Afive \Afive                |
      \Cfive   \Dfive   | \Efive   \Efive   | \Dfive   \Dfive  | \Gfiveii \Ffiveii            |
      \Gfiveii \Ffiveii | \Gfiveii \Ffiveii | \Gfiveii \Dseven | g,8^5 g8^1 c'8^3 d'8^2 g'2^1 |
    }
    \chords {
      c1:5      | c1:5      | c1:5      | c2:5 r2   |
      e1:5      | f2:5 g2:5 | c1:5      | a1:5      |
      c2:5 d2:5 | e1:5      | d1:5      | g2:5 f2:5 |
      g2:5 f2:5 | g2:5 f2:5 | g2:5 d2:7 | r1        |
    }
  >>
  \layout {}
  \midi {}
}
