\version "2.24.3"

#(define title      "明天，你好")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 20")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

CI  = { c8  g8  c'8 g8  c'8 g8  c'8 g8  }
CII = { e,8 c8  e8  c8  e8  c8  e8  c8  }
DmI = { d,8 a,8 d8  a,8 d8  a,8 d8  a,8 }
EmI = { g,8 e8  g8  e8  g8  e8  g8  e8  }
FI  = { f,8 c8  f8  c8  f8  c8  f8  c8  }
GI  = { b,8 g8  b8  g8  b8  g8  b8  g8  }
GII = { g,8 d8  g8  d8  g8  d8  g8  d8  }
AmI = { a,8 e8  a8  e8  a8  e8  a8  e8  }

GX = { g,8 d8 g8 d8 a8 d8 b8 d8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      \A
      r4  r8 c''8 c''8 d''8 e''8 d''8~ | d''4 g''8 g''8~ g''8 b'4       c''8~ | c''4 r8 a'8 a'8 b'8 c''8 b'8~ | b'4 e''8 e''8~ e''8 g'4 a'8~ | \break
      a'4 r4      a'8  c''8 f''8 e''8~ | e''4 e''8 c''8~ c''8 d''8 e''8 d''8~ | d''2        r8  g'8 e''4      | d''2           r2            | \break
      
      r4  r8 c''8 c''8 d''8 e''8 d''8~ | d''4 g''8 g''8~ g''8 b'4       c''8~ | c''4      r8   a'8  a'8  b'8  c''8 b'8~  | b'4  e''8 e''8~ e''8 g'4  a'8~  | \break
      a'4 r4      a'8  c''8 f''8 e''8~ | e''4 g''8 c''8~ c''8 d''8 e''8 f''8~ | f''8 e''8 f''8 e''8 f''8 g''8 e''8 d''8~ | d''4 r8   g'8   d''8 c''4 e''8~ | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \CI | \GI  | \AmI | \EmI |
      \FI | \CII | \DmI | \GX  |
      
      \CI | \GI  | \AmI | \EmI |
      \FI | \CII | \DmI | \GII |
    }
    \chords {
      
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | d1:m | g1   |
      
      c1 | g1 | a1:m | e1:m |
      f1 | c1 | d1:m | g1   |
    }
  >>
  \layout {}
  \midi {}
}
