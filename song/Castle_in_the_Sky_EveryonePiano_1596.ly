\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Castle in the Sky"
  tagline = "EveryonePiano 1596"
}

\paper {
  total-page = 2
}

C     = { c8  e8  g2.  }
Dm    = { d8  f8  a2.  }
Em    = { e8  g8  b2.  }
F     = { f8  a8  c'2. }
AmI   = { a8  c'8 e'2. }
AmII  = { a,8 c8  e2.  }
Bfive = { b,8 fs8 b2.  }

\markup \vspace #1.5

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      \partial 4 a'8 b'8 | c''4. b'8 c''4 e''4 | b'2. e'4              | a'4. g'8 a'4 c''4     | g'2. \break
                 e'8 e'8 | f'4. e'8 f'8  c''4. | e'2 r8 c''8 c''8 c''8 | b'4. fs'8 fs'4 b'4    | b'2. \break
                 a'8 b'8 | c''4. b'8 c''4 e''4 | b'2. e'4              | a'4. g'8 a'4 c''4     | g'2. \break
                 e'8 e'8 | f'4 c''8 b'4. c''4  | d''4 e''8 c''8~ c''2  | c''8 b'8 a'4 b'4 gs'4 | a'2. \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      r4 | \AmI | \Em   | \F                  | \C                      |
         | \Dm  | \C    | \Bfive              | e,8 b,8 e8 gs8 b4 e'4   |
         | \AmI | \Em   | \F                  | \C                      |
         | \Dm  | \AmII | d8 a8 d'4 <e gs b>2 | <a c' e'>2.\arpeggio r4 |
         |
    }
    \chords {
      r4 | a1:m | e1:m | f1      | c1       |
         | d1:m | c1   | b1:5    | e1       |
         | a1:m | e1:m | f1      | c1       |
         | d1:m | c1   | d2:5 e2 | a2.:m r4 |
         |
    }
  >>
  \layout {}
  \midi {}
}
