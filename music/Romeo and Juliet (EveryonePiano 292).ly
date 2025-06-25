\version "2.24.3"

#(define title      "Romeo and Juliet")
#(define title-font "")
#(define sequence   "EveryonePiano 292")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

C  = { c,8  g,8 ef8 g,8 ef8 g,8 ef8 g,8 }
F  = { f,8  c8  af8 c8  af8 c8  af8 c8  }
G  = { g,8  d8  bf8 d8  bf8 d8  bf8 d8  }
Am = { af,8 ef8 c'8 ef8 c'8 ef8 c'8 ef8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 69
      \clef treble
      \key ef \major
      \time 4/4
      
      r2 r8 c''8 ef''8 d''8 | g'2~ g'8  g'8  bf'8 g'8                            | c''2. c''4 | f''1 | \break
      d''2.      g'4        | ef''4. d''8 c''8 bf'8 \tuplet 3/2 { ef'' d'' c'' } | bf'1       | c''2 r8 c''8 ef''8. d''16 | \break
    }
    \new Staff {
      \clef bass
      \key ef \major
      \time 4/4
      
      \C | \G | \Am | \F |
      \G | \C | \G  | \C |
    }
    \chords {
      
      c1 | g1 | a1:m | f1 |
      g1 | c1 | g1   | c1 |
    }
  >>
  \layout {}
  \midi {}
}
