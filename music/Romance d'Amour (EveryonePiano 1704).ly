\version "2.24.3"

#(define title      "Romance d'Amour")
#(define title-font "")
#(define sequence   "EveryonePiano 1704")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

"E15850" = { e,8 b,8 e8 b,8 gs4  }
"A15850" = { a,8 e8  a8 e8  cs'4 }

"D1585b0" = { d,8 a,8 d8 a,8 f4  }
"A1585b0" = { a,8 e8  a8 e8  c'4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      e''4^5 e''4 e''4 | e''4  d''4 c''4 | c''4   b'4  a'4  | a'4  c''4 e''4 | \break
      a''4^5 a''4 a''4 | a''4  g''4 f''4 | f''4   e''4 d''4 | d''4 e''4 f''4 | \break
      e''4   f''4 e''4 | gs''4 f''4 e''4 | e''4^5 d''4 c''4 | c''4 b'4  a'4  | \break
      b'4    b'4  b'4  | b'4   c''4 b'4  | a'4    a'4  a'4  | \acciaccatura a'8 <a' a''>2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \magnifyMusic 1 {
        \"A1585b0" | \"A1585b0" | \"A1585b0" | \"A1585b0" |
        \"A15850"  | \"A15850"  | \"D1585b0" | \"D1585b0" |
        \"E15850"  | \"E15850"  | \"A1585b0" | \"A1585b0" |
        \"E15850"  | \"E15850"  | \"A1585b0" | <a, e a>2. |
      }
    }
    \chords {
      a2.:m | a2.:m | a2.:m | a2.:m |
      a2.   | a2.   | d2.:m | d2.:m |
      e2.   | e2.   | a2.:m | a2.:m |
      e2.   | e2.   | a2.:m | a2.:m |
    }
  >>
  \layout {}
  \midi {}
}