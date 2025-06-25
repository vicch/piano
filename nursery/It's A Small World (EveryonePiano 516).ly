\version "2.24.3"

#(define title      "It's A Small World")
#(define title-font "")
#(define sequence   "EveryonePiano 516")
#(define total-page 1)

\include "../base.ly"

\paper {
  ragged-last = ##t
}

\markup \vspace #1.5

Di = { d4 a4 d'2  }
Am = { e4 a4 cs'2 }

Dii = { <<fs4 a4>>   d4 <<fs4 a4>>   d4 }
G   = { <<g4  b4>>   d4 <<g4  b4>>   d4 }
A   = { <<a4  cs'4>> e4 <<a4  cs'4>> e4 }

Diii = { d'8 a8 fs8 a8 d2 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key d \major
      \time 4/4
      
      \partial 4  fs'8 g'8 | a'4 fs''4     d''4  e''8 d''8 | d''4 cs''4      cs''4 e'8   fs'8 | g'4 e''4 cs''4 d''8 cs''8 | \break
      b'4 a'4 a'4 fs'8 g'8 | a'4 d''8 e''8 fs''4 e''8 d''8 | b'4  e''8 fs''8 g''4  fs''8 e''8 | a'4 g''4 fs''4.     e''8  | \break
      
      d''1               | d''4.  d''8  fs''4 d''4  | e''4. e''8 e''2            | e''4. e''8 g''4 e''4 | \break
      fs''4. fs''8 fs''2 | fs''4. fs''8 a''4  fs''4 | g''4. g''8 g''4 fs''8 e''8 | a'2        cs''2     | \break
      
      d''1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key d \major
      \time 4/4
      
      r4  | \Di          | \Am         | \Am                           |
      \Di | d4 a4 d'4 a4 | g4 b4 e4 b4 | <<a4 cs'4>> e4 <<g4 cs'4>> e4 |
      
      \Diii | \Dii | \A | \A                    |
      \Dii  | \Dii | \G | <e a cs'>2 <g a cs'>2 |
      
      \Diii |
    }
    \chords {
      
      r4 | d1 | a1:m | a1:m |
      d1 | d1 | e1:m | r1   |
      
      d1 | d1 | a1 | a1    |
      d1 | d1 | g1 | a2 r2 |
      
      d1 |
    }
  >>
  \layout {}
  \midi {}
}
