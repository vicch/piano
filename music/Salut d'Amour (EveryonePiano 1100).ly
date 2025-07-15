\version "2.24.3"

#(define title      "Salut d'Amour")
#(define title-font "")
#(define sequence   "EveryonePiano 1100")
#(define total-page 1)

\include "../base.ly"

\paper {
  ragged-last = ##t
}

\markup \vspace #1.5

"C1313" = { c'4 e'4 c'4 e'4 }
"D1313" = { d'4 f'4 d'4 f'4 }
"F3131" = { a4  f'4 a4  f'4 }

"D1535" = { fs4 d'4 a4   d'4 }
"A1535" = { a4  e'4 cs'4 e'4 }

"E5151" = { b4 e'4 b4 e'4 }
"A1515" = { a4 e'4 a4 e'4 }

"Ab351b3" = { c'4 e'4 a4 c'4 }

"B1b51b5" = { b4 f'4 b4 f'4 }

"Bb5b31b3" = { f4 d'4 b4 d'4 }

"Eb31b31" = { g4 e'4 g4 e'4 }

"G1b71b7" = { g4 f'4 g4 f'4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      \repeat volta 2 {
        e''2^4 g'4^1  e''4 | d''4 c''4 b'4 c''4 | f''2   f''2 | f''2 g'2^1     | \break
        e''2^5 gs'4^2 e''4 | d''4 c''4 b'4 c''4 | d''2   d''2 | d''2 ds''2^5   | \break
        e''2^4 g'4^1  e''4 | d''4 c''4 b'4 c''4 | a''2^5 a''2 | a''2 g''4 f''4 | \break
        
        e''2 d''4 c''4^3 | a'2^1 b'2 |
        \alternative {
          \volta 1 {
            c''2 f'2^1 | fs'2^2 g'2^1 | \break
          }
          \volta 2 {
            c''1~ | c''1 | \bar "|."
          }
        }
      }
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \repeat volta 2 {
        \"C1313" | \"E5151" | \"F3131" | \"B1b51b5"  |
        \"C1313" | \"A1515" | \"D1535" | \"Bb5b31b3" |
        \"C1313" | \"E5151" | \"A1535" | \"D1313"    |
        
        \"Eb31b31" | \"G1b71b7" |
        \alternative {
          \volta 1 {
            \"Ab351b3" | d4 c'4 b4 d'4 |
          }
          \volta 2 {
            c'4^1 e4^4 fs4^3 g4^2 | c1^5 |
          }
        }
      }
    }
    \chords {
      c1 | e1 | f1 | b1:sus |
      c1 | a1 | d1 | b1:dim |
      c1 | e1 | a1 | d1:m   |
      
      e1:m | g1:7 |
      a1:m |
    }
  >>
  \layout {}
  \midi {}
}
