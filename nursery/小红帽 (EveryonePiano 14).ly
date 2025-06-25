\version "2.24.3"

#(define title      "小红帽")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 14")
#(define total-page 2)

\include "../base.ly"

\markup \vspace #1.5

Ci        = { c8  <e  g>8 c8  <e  g>8 }
F         = { c8  <f  a>8 c8  <f  a>8 }
G         = { g,8 <b, d>8 g,8 <b, d>8 }
Gsevensus = { g,8 <d  f>8 g,8 <c  e>8 }

Cii = { c8 <e g>8 c4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 2/4
      
      c'8^1 d'8 e'8 f'8 | g'4     e'8 c'8 | c''4^5 a'8 f'8 | g'8 g'8 e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | d'4     g'4   | \break
      c'8   d'8 e'8 f'8 | g'4     e'8 c'8 | c''4^5 a'8 f'8 | g'4     e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | c'4     c'4   | \break
      c''4^5    a'8 f'8 | g'8 g'8 c'4^1   | c''4   a'8 f'8 | g'4     e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | c'4     c'4   | \break
      c''4^5    a'8 f'8 | g'8 g'8 c'4^1   | c''4   a'8 f'8 | g'4     e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | c'4     c'4   | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 2/4
      
      \Ci | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \G   |
      \Ci | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \Ci  |
      \F  | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \Cii |
      \F  | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \Cii |
    }
    \chords {
      c2 | c2 | f2       | c2 |
      c2 | c2 | g2:7sus4 | g2 |
      c2 | c2 | f2       | c2 |
      c2 | c2 | g2:7sus4 | c2 |
      f2 | c2 | f2       | c2 |
      c2 | c2 | g2:7sus4 | c2 |
      f2 | c2 | f2       | c2 |
      c2 | c2 | g2:7sus4 | c2 |
    }
  >>
  \layout {}
}

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 2/4
      
      c'8^1 d'8 e'8 f'8 | g'4     e'8 c'8 | c''4^5 a'8 f'8 | g'8 g'8 e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | d'4     g'4   | \break
      c'8   d'8 e'8 f'8 | g'4     e'8 c'8 | c''4^5 a'8 f'8 | g'4     e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | c'4     c'4   | \break
      c''4^5    a'8 f'8 | g'8 g'8 c'4^1   | c''4   a'8 f'8 | g'4     e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | c'4     c'4   | \break
      c''4^5    a'8 f'8 | g'8 g'8 c'4^1   | c''4   a'8 f'8 | g'4     e'4^1 | \break
      c'8^1 d'8 e'8 f'8 | g'8 e'8 d'8 c'8 | d'4    e'4     | c'4     c'4   | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 2/4
      
      \Ci | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \G   |
      \Ci | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \Ci  |
      \F  | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \Cii |
      \F  | \Ci | \F         | \Ci  |
      \Ci | \Ci | \Gsevensus | \Cii |
    }
  >>
  \midi {}
}
