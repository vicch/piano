\version "2.24.3"

#(define title      "茉莉花")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 518")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

CI  = { c8  g8  c'8 g8  }
DI  = { d8  a8  d'8 a8  }
DII = { d8  fs8 a8  c'8 }
EI  = { e8  b8  e'8 b8  }
FI  = { f8  c'8 f'8 c'8 }
FII = { f,8 c8  f8  c8  }
GI  = { g8  d'8 g'8 d'8 }
GII = { g,8 d8  g8  d8  }
AI  = { a,8 e8  a8  e8  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      e''4^1 e''8 g''8^2 a''8 c'''8 c'''8 a''8 | g''4 g''8 a''8 g''2 | e''4   e''8 g''8 a''8 c'''8 c'''8 a''8 | g''4 g''8 a''8 g''2 | \break
      g''4^2 g''4        g''4       e''8  g''8 | a''4 a''4      g''2 | e''4^3 d''8 e''8 g''4       e''8  d''8 | c''4 c''8 d''8 c''2 | \break

      e''8^3 d''8 c''8 e''8 d''4. e''8^1 | g''4^2 a''8 c'''8 g''2 | d''4^2 e''8 g''8 d''8^3 e''8 c''8^3 a'8 | g'2 a'4^2 a'8 c''8^3 | \break

      d''4. e''8 c''8 d''8 c''8 a'8 | g'2 a'4 a'8 c''8 | d''4. e''8 c''8^2 d''8 c''8 a'8 | g''2^5 <b'' d''' g'''>2\arpeggio | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \CI  \CI  | \CI  \CI  | \CI  \CI  | \CI c8^5 g8^2 c8^5 d8^4 |
      \EI  \EI  | \FI  \GI  | \CI  \CI  | \AI \AI                 |

      \CI  \DI  | \EI  \EI  | \DI  \DI  | \GII \FII |

      \GII \FII | \GII \FII | \GII \DII | g,8^5 g8^1 c'8^3 d'8^2 g'2^1 |
    }
    \chords {
      c1 | c1    | c1 | c2 r2 |
      e1 | f2 g2 | c1 | a1    |

      c2 d2 | e1 | d1 | g2 f2 |

      g2 f2 | g2 f2 | g2 d2 | r1 |
    }
  >>
  \layout {}
  \midi {
    \context {
      \ChordNames
      \remove "Note_performer"
    }
  }
}
