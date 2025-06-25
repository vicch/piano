\version "2.24.3"

#(define title      "遇见")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 68")
#(define total-page 1)

\include "../base.ly"

\paper {
  ragged-last = ##t
}

\markup \vspace #1.5

CI   = { c8  g8  c'4 }
DI   = { d8  a8  d'4 }
GI   = { b,8 g8  b4  }
GII  = { g,8 d8  g4  }
GIII = { g8  d'8 g'4 }
FI   = { f,8 c8  f4  }
FII  = { f8  c'8 f'4 }

CII = { c8  g8 c'8 d'8 e'2 }
AmI = { a,8 e8 a8  b8  c'2 }

FIII = { f,8 c8 f8 c8 }
GIV  = { g,8 d8 g8 d8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 88
      \clef treble
      \key c \major
      \time 4/4
      
      r2 r4  g''8^5 e''8(   | e''4) g''8 d''8(    d''4)  e''8  d''8( | d''8) c''2  r8 c''8^3 b'8 | a'8 b'8 c''8 b'8( b'8) c''8 d''8 e''8( | \break
      e''2.) g''8^2 e''8^1( | e''4) g''8 d'''8^5( d'''4) c'''8 b''8( | b''8) c'''2 r8 c''8^3 b'8 | a'8 b'8 c''8 b'8( b'8) c''8 d''4       | \break

      c''2        r8 g''8^1 a''8 b''8 | c'''4 b''8   c'''8 b''8  a''8  g''8  a''8(  | a''8)  g''4.   r8 c''8^1 d''8 e''8 | f''4 e''8 f''8 g''8 c''8 d''8 e''8( | \break
      e''8) e''4. r8 g''8^1 a''8 b''8 | c'''4 b''8^2 c'''8 d'''8 c'''8 d'''8 e'''8( | e'''8) g''4.^1 r8 c''8^2 d''8 e''8 | f''4 e''8 f''8 e''8 d''4      c''8  | \break
      
      b'8 c''4.( c''2) | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      r1   | \CI \GI | \AmI | \FI   \GII |
      \CII | \CI \GI | \AmI | \FIII \GIV |
      
      \CII | \FII \GIII | \CII             | \DI \GII |
      \CII | \FII \GIII | c8 g8 b,8 g8 a,2 | \DI \GII |
      
      \CII |
    }
    \chords {

      r1 | c2 g2 | a1:m | f2 g2 |
      c1 | c2 g2 | a1:m | f2 g2 |
      
      c1 | f2 g2 | c1 | d2 g2 |
      c1 | f2 g2 | r1 | d2 g2 |
      
      c1 |
    }
  >>
  \layout {}
}

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 88
      \clef treble
      \key c \major
      \time 4/4
      
      r2 r4  g''8 e''8( | e''4) g''8 d''8(  d''4)  e''8  d''8( | d''8) c''2  r8 c''8 b'8 | a'8 b'8 c''8 b'8( b'8) c''8 d''8 e''8( | \break
      e''2.) g''8 e''8( | e''4) g''8 d'''8( d'''4) c'''8 b''8( | b''8) c'''2 r8 c''8 b'8 | a'8 b'8 c''8 b'8( b'8) c''8 d''4       | \break

      c''2        r8 g''8 a''8 b''8 | c'''4 b''8 c'''8 b''8  a''8  g''8  a''8(  | a''8)  g''4. r8 c''8 d''8 e''8 | f''4 e''8 f''8 g''8 c''8 d''8 e''8( | \break
      e''8) e''4. r8 g''8 a''8 b''8 | c'''4 b''8 c'''8 d'''8 c'''8 d'''8 e'''8( | e'''8) g''4. r8 c''8 d''8 e''8 | f''4 e''8 f''8 e''8 d''4      c''8  | \break
      
      b'8 c''4.( c''2) | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      r1   | \CI \GI | \AmI | \FI   \GII |
      \CII | \CI \GI | \AmI | \FIII \GIV |
      
      \CII | \FII \GIII | \CII             | \DI \GII |
      \CII | \FII \GIII | c8 g8 b,8 g8 a,2 | \DI \GII |
      
      \CII |
    }
  >>
  \midi {}
}
