\version "2.24.3"
\include "../template.v1.ly"

\paper {
  ragged-last = ##t
}

\header {
  title = \markup \override #'((font-size . 6)) "Salut d'Amour"
  tagline = "EveryonePiano 1100"
}

\markup \vspace #1.5

chordc     = { c'4( e'4 c'4  e'4) }
chordd     = { fs4( d'4 a4   d'4) }
chorddm    = { d'4( f'4 d'4  f'4) }
chordem    = { g4(  e'4 g4   e'4) }
chordefive = { b4(  e'4 b4   e'4) }
chordf     = { a4(  f'4 a4   f'4) }
chordfsus  = { g4(  f'4 g4   f'4) }
chorda     = { a4(  e'4 cs'4 e'4) }
chordam    = { c'4( e'4 a4   c'4) }
chordafive = { a4(  e'4 a4   e'4) }
chordbm    = { f4(  d'4 b4   d'4) }
chordbsus  = { b4(  f'4 b4   f'4) }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      \repeat volta 2 {
        e''2^4 g'4^1  e''4^4 | d''4^3 c''4^2 b'4^1 c''4^2 | f''2^5 f''2 | f''2 g'2^1         | \break
        e''2^5 gs'4^2 e''4^5 | d''4^4 c''4^3 b'4^2 c''4^3 | d''2^4 d''2 | d''2 ds''2^5       | \break
        e''2   g'4    e''4   | d''4\< c''4   b'4   c''4\! | a''2^5 a''2 | a''2 g''4^4 f''4^3 | \break
        e''2^2 d''4^1 c''4^2 | a'2^1         b'2^2        |
        \alternative {
          \volta 1 {
            c''2^3 f'2^1 | fs'2^2_"rit." g'2^1 | \break
          }
          \volta 2 {
            c''1~^3\> | c''1\! | \bar "|."
          }
        }
      }
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \repeat volta 2 {
        \chordc  | \chordefive | \chordf | \chordbsus |
        \chordc  | \chordafive | \chordd | \chordbm   |
        \chordc  | \chordefive | \chorda | \chorddm   |
        \chordem | \chordfsus  |
        \alternative {
          \volta 1 {
            \chordam | d4( c'4 b4 d'4) |
          }
          \volta 2 {
            c'4^1( e4^3 fs4^2 g4^1 | c1^5) |
          }
        }
      }
    }
    \chords {
      \set noChordSymbol = ""
      
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
          \chordc  | \chordefive | \chordf | \chordbsus |
          \chordc  | \chordafive | \chordd | \chordbm   |
          \chordc  | \chordefive | \chorda | \chorddm   |
          \chordem | \chordfsus  |
          \alternative {
            \volta 1 {
              \chordam | d4( c'4 b4 d'4) |
            }
            \volta 2 {
              c'4( e4 fs4 g4 | c1) |
            }
          }
        }
      }
    >>
  }
  \midi {}
}
