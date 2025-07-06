\version "2.24.3"

#(define title      "白桦林")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 1056")
#(define total-page 2)

\include "../base.ly"

\markup \vspace #1.5

CI  = { c4  <<e4  g4>>  <<e4  g4>>  }
DmI = { d4  <<f4  a4>>  <<f4  a4>>  }
EI  = { e4  <<gs4 b4>>  <<gs4 b4>>  }
EmI = { e,4 <<g,4 b,4>> <<g,4 b,4>> }
GI  = { g,4 <<b,4 d4>>  <<b,4 d4>>  }
AmI = { a,4 <<c4  e4>>  <<c4  e4>>  }

AmII = { <a, c e>2.\arpeggio }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      e'4.^1  f'8  e'4       | c''2^5    a'4    | b'4.  c''8  b'8    a'8  | e'2.   | \break
      d'4.^1  e'8  d'4       | b'4^5 a'4 d'4    | e'4   gs'4  b'4         | a'2.   | \break
      a'4^1   bf'4 a'4       | a''2^5    e''4^2 | f''4. g''8  f''8   d''8 | e''2.  | \break
      e''4.^3 c''8 d''8 e''8 | d''2      c''4   | b'4^2 e'4^1 e''8^5 d''8 | a'2.^1 | \break
      
      a''4.^5 e''8 e''8  f''8 | f''4.        d''8^2 a'8^1 d''8 | g''4^4    g''8 a''8  g''8   a''8   | e''2.^2 | \break
      e''4.^5 d''8 c''8  b'8  | e'4^1 d''8^5 c''8   b'8   a'8  | b'8^1 b'8 b'8 e''8^3 e''8   d''8^2 | e''2.   | \break
      a''4.^3 b''8 c'''8 b''8 | f''4.        d''8^2 a'8^1 d''8 | g''4^3    a''4       b''4          | e''2.^1 | \break
      e''4.^3 c''8 d''8  e''8 | d''2                c''4       | b'4^2     e'4^1      e''8^5 d''8   | a'2.^1~ | a'2.~ | a'2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \EI  | \AmI | \EI  | \EI | \DmI | \DmI | \EI | \AmI |
      \AmI | \AmI | \DmI | \EI | \AmI | \EI  | \EI | \AmI |
      
      \AmI | \DmI | \GI | \CI | \EI | \EI | \EI | \EI  |
      \AmI | \DmI | \GI | \CI | \CI | \EI | \EI | \AmI | \EmI | \AmII |
    }
    \chords {
      e2.   | a2.:m | e2.   | e2. | d2.:m | d2.:m | e2. | a2.:m |
      a2.:m | a2.:m | d2.:m | e2. | a2.:m | e2.   | e2. | a2.:m |
      
      a2.:m | d2.:m | g2. | c2. | e2. | e2. | e2. | e2.   |
      a2.:m | d2.:m | g2. | c2. | c2. | e2. | e2. | a2.:m | e2.:m | a2.:m |
    }
  >>
  \layout {}
  \midi {}
}
