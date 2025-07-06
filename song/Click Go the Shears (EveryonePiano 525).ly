\version "2.24.3"

#(define title      "Click Go the Shears")
#(define title-font "")
#(define sequence   "EveryonePiano 525")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

CI = { c4  <g c' e'>4-. <g c' e'>4-. <g c' e'>4-. }
FI = { f,4 <f a  c'>4-. <f a  c'>4-. <f a  c'>4-. }
GI = { g,4 <g b  d'>4-. <g b  d'>4-. <g b  d'>4-. }

CII = { <e'' g'' c'''>4-! }
GII = { <g   b   d'>2 }

CII  = { c''4 <e'' g'' c'''>4-! <e'' g'' c'''>4-! r4 }
CIII = { c4   <g   c'  e'>4-!   <g   c'  e'>4-!   r4 }

CIV = { c4  <g c' e'>4-. }
GIV = { g,4 <g b  d'>4-. }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      e''4 e''8. d''16 c''8 c''8 e''8 g''8 | c'''4 c'''8. b''16 a''2 | g''4          g''8. a''16 g''4      e''8. c''16 | d''4 d''8. e''16 d''2 | \break
      e''4 e''8. d''16 c''8 c''8 e''8 g''8 | c'''4 c'''8. b''16 a''2 | d'''8. c'''16 b''8  a''8  g''8 f''8 e''8  d''8  | \CII                  | \break
      
      d'''4     d'''8. c'''16 b''4      d'''4     | c'''4 e'''4        c'''2 | a''4          a''8. b''16 c'''4     a''4      | g''4 c'''4 d''2 | \break
      e''8 e''8 e''8 d''8     c''8 c''8 e''8 g''8 | c'''4 c'''8. b''16 a''2  | d'''8. c'''16 b''8 a''8   g''8 f''8 e''8 d''8 | \CII            | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \CI | \FI | \CI     | \GI   |
      \CI | \FI | \GII r2 | \CIII |
      
      \GI | \CI | \FI     | \CIV       \GIV    |
      \CI | \FI | \GII r2 | c'4-! g4-! c4-! r4 | 
    }
    \chords {
      c1 | f1 | c1    | g1     |
      c1 | f1 | g2 r2 | c2. r4 |
      
      g1 | c1 | f1    | c2 g2  |
      c1 | f1 | g2 r2 | c2. r4 |
    }
  >>
  \layout {}
  \midi {}
}
