\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "小白船"
  tagline = "EveryonePiano 512"
}

\paper {
  total-page = 1
}

\markup \vspace #1.25

Ci        = { c'4 e'4 g'4 }
Cii       = { g4  c'4 e'4 }
Fi        = { f4  a4  c'4 }
Fii       = { f4  c'4 f'4 }
G         = { g4  b4  d'4 }
Gsevensus = { g4  d'4 f'4 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      g''2^4 a''4^5 | g''2^4 e''4^2 | g''4^5 e''8^4 d''8^3 c''4^2 | g'2.^1 |
      a'2^1  c''4^2 | d''2^3 g''4^5 | e''2.~^4                    | e''2.  | \break
      g''2   a''4   | g''2   e''4   | g''4   e''8   d''8   c''4   | g'2.   |
      a'2^2  c''4^4 | g'2^1  d''4^5 | c''2.~^4                    | c''2.  | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \Ci  | \Ci        | \Ci  | \Cii |
      \Fi  | \G         | \Cii | \Cii |
      \Ci  | \Ci        | \Ci  | \Cii |
      \Fii | \Gsevensus | \Ci  | \Ci  |
      
    }
    \chords {
      c2. | c2.       | c2. | c2. |
      f2. | g2.       | c2. | c2. |
      c2. | c2.       | c2. | c2. |
      f2. | g2.:7sus4 | c2. | c2. |
    }
  >>
  \layout {}
  \midi {}
}
