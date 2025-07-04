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

C     = { c'4 e'4 c'4  e'4 }
D     = { fs4 d'4 a4   d'4 }
Dm    = { d'4 f'4 d'4  f'4 }
Em    = { g4  e'4 g4   e'4 }
Efive = { b4  e'4 b4   e'4 }
F     = { a4  f'4 a4   f'4 }
Fsus  = { g4  f'4 g4   f'4 }
A     = { a4  e'4 cs'4 e'4 }
Am    = { c'4 e'4 a4   c'4 }
Afive = { a4  e'4 a4   e'4 }
Bm    = { f4  d'4 b4   d'4 }
Bsus  = { b4  f'4 b4   f'4 }

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
        e''2^4 g'4^1  e''4   | d''4 c''4 b'4 c''4 | f''2   f''2 | f''2 g'2^1     | \break
        e''2^5 gs'4^2 e''4   | d''4 c''4 b'4 c''4 | d''2   d''2 | d''2 ds''2^5   | \break
        e''2^4 g'4^1  e''4   | d''4 c''4 b'4 c''4 | a''2^5 a''2 | a''2 g''4 f''4 | \break
        e''2   d''4   c''4^3 | a'2^1       b'2        |
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
        \C  | \Efive | \F | \Bsus |
        \C  | \Afive | \D | \Bm   |
        \C  | \Efive | \A | \Dm   |
        \Em | \Fsus  |
        \alternative {
          \volta 1 {
            \Am | d4 c'4 b4 d'4 |
          }
          \volta 2 {
            c'4^1 e4^4 fs4^3 g4^2 | c1^5 |
          }
        }
      }
    }
    \chords {
      c1   | e1:5   | f1 | b1:sus |
      c1   | a1:5   | d1 | b1:m   |
      c1   | e1:5   | a1 | d1:m   |
      e1:m | f1:sus |
    }
  >>
  \layout {}
}

\score {
  \unfoldRepeats {
    \new PianoStaff <<
      \new Staff {
        \tempo 4 = 96
        \clef treble
        \key c \major
        \time 4/4
        
        \repeat volta 2 {
          e''2 g'4  e''4 | d''4   c''4 b'4 c''4   | f''2 f''2 | f''2 g'2       | \break
          e''2 gs'4 e''4 | d''4   c''4 b'4 c''4   | d''2 d''2 | d''2 ds''2     | \break
          e''2 g'4  e''4 | d''4\< c''4 b'4 c''4\! | a''2 a''2 | a''2 g''4 f''4 | \break
          e''2 d''4 c''4 | a'2         b'2        |
          \alternative {
            \volta 1 {
              c''2 f'2 | fs'2_"rit." g'2 | \break
            }
            \volta 2 {
              c''1~\> | c''1\! | \bar "|."
            }
          }
        }
      }
      \new Staff {
        \clef bass
        \key c \major
        \time 4/4
        
        \repeat volta 2 {
          \C  | \Efive | \F | \Bsus |
          \C  | \Afive | \D | \Bm   |
          \C  | \Efive | \A | \Dm   |
          \Em | \Fsus  |
          \alternative {
            \volta 1 {
              \Am | d4( c'4 b4 d'4) |
            }
            \volta 2 {
              c'4^1( e4^4 fs4^3 g4^2 | c1^5) |
            }
          }
        }
      }
    >>
  }
  \midi {}
}
