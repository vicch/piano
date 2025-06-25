\version "2.24.3"

#(define title      "Castle in the Sky")
#(define title-font "")
#(define sequence   "EveryonePiano 1596")
#(define total-page 2)

\include "../base.ly"

\markup \vspace #1.5

C     = { c8  e8  g2.  }
Dm    = { d8  f8  a2.  }
Em    = { e8  g8  b2.  }
F     = { f8  a8  c'2. }
AmI   = { a8  c'8 e'2. }
AmII  = { a,8 c8  e2.  }
Bfive = { b,8 fs8 b2.  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      \partial 4 a'8^1  b'8  | c''4.        b'8  c''4 e''4    | b'2.          e'4^1     | a'4.^3 g'8     a'4  c''4 | \break
      g'2.       e'8^1  e'8  | f'4.         e'8  f'8  c''4.^5 | e'2 r8 c''8^5 c''8 c''8 | b'4.   fs'8^2  fs'4 b'4  | \break
      b'2.       a'8^1  b'8  | c''4.        b'8  c''4 e''4    | b'2.          e'4^1     | a'4.^3 g'8     a'4  c''4 | \break
      g'2.       e'8^1  e'8  | f'4 c''8^5   b'4.^2    c''4    | d''4 e''8 c''8~ c''2    | c''8^5 b'8 a'4 b'4  gs'4 | \break
      a'2.       c''8^1 d''8 | e''4.        d''8 e''4 g''4    | d''2.         g'4       | c''4.  b'8     c''4 e''4 | \break
      e''2.      g'8    g'8  | a'8 b'8 c''4 b'8  c''8 d''4    | c''4.     g'8   g'2     | <<d''4 f''4>> <<c''4 e''4>> <<b'4 d''4>> <<a'4 c''4>> | \break
      <<b'2. e''2.>> e''4    | a''2         g''2              | e''8 d''8 c''2 c''4     | d''4.  c''8    d''4 g''4 | \break
      e''2.          e''4    | a''2         g''2              | e''8 d''8 c''2 c''4     | d''4.  c''8    d''4 b'4  | <e' a'>1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      r4 | \AmI | \Em | \F     |
      \C | \Dm  | \C  | \Bfive |
      
      e,8 b,8 e8 gs8 b4 e'4 | \AmI | \Em   | \F                  |
      \C                    | \Dm  | \AmII | d8 a8 d'4 <e gs b>2 |
      
      <a c' e'>2.\arpeggio r4 | c8 e8 g2 c'4        | g,8 b,8 d2 r4 | a,8 e8 a2 c'4 |
      e,8 b,8 e4 g2           | <f a c'>2 <f b d'>2 | <e g c'>1     | <d a c'>1     |
      
      e,4   gs,8 b,8 e8 gs8 b8 e'8 | a,8 e8 a4 e,8 b,8 g4 | f,8 c8 f8 a8 b4 g4 | g,8 d8 f4 a4  c'4  |
      c8 e8 g8   c'8 d'4    r4     | a,8 e8 a4 e,8 b,8 g4 | f,8 c8 f8 a8 b4 g4 | <b, d f>2 b,4 gs,4 | <a, c e>1 |
    }
    \chords {
      r4 | a1:m | e1:m | f1   |
      c1 | d1:m | c1   | b1:5 |
      
      e1 | a1:m | e1:m | f1      |
      c1 | d1:m | a1:m | d2:5 e2 |
      
      a2.:m r4 | c1    | g1 | a1:m |
      e1:m     | f2 r2 | c1 | r1   |
      
      r1 | a2:5 e2:m | r1 | r1 |
      r1 | a2:5 e2:m | r1 | r1 | a1:m |
    }
  >>
  \layout {}
  \midi {}
}
