\version "2.24.3"

#(define title      "Canon")
#(define title-font "")
#(define sequence   "EveryonePiano 31")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

"C58a"  = { c8  g8 c'8 e'8 }
"F58a"  = { f,8 c8 f8  a8  }
"G58a"  = { g,8 d8 g8  b8  }
"Am58a" = { a,8 e8 a8  c'8 }

"C358" = { c8 e8 g8 c'8 }

"G368" = { b,8 d8 g8 b8 }

"Em8ac" = { e,8 e8 g8 b8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 88
      \clef treble
      \key c \major
      \time 4/4
      
      e'2 d'2 | c'2 b2 | a2 g2 | a2 b2 | <g' e''>2 <g' d''>2 | <e' c''>2 <e' b'>2 | <c' a'>2 <c' g'>2 | <c' a'>2 <d' b'>2 | \break
      
      <g' e''>2 <g' d''>4 f'4 | c''2 b'4 g'4 | a'2 g'4 e'4 | <f' a'>2 <d' g'>4 f'4 | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      c2 g,2 | a,2 e,2 | f,2 g,2 | f,2 g,2 | c2 g,2 | a,2 e,2 | f,2 c2 | f,2 g,2 |
      
      \"C58a" \"G368" | \"Am58a" \"Em8ac" | \"F58a" \"C358" | \"F58a" \"G58a" |
    }
    \chords {
      r1 | r1 | r1 | r1 | r1 | r1 | r1 | r1 |
      
      c2 g2 | a2:m e2:m | f2 c2 | f2 g2 |
    }
  >>
  \layout {}
  \midi {}
}
