\version "2.24.3"

#(define title      "Minuet in G Major")
#(define title-font "")
#(define sequence   "EveryonePiano 55")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key g \major
      \time 3/4
      
      \A
      
      d''4 g'8  a'8  b'8 c''8 | d''4-. g'4-.    g'4-.   | e''4 c''8 d''8 e''8 fs''8 | g''4-. g'4-. g'4-.     | \break
      c''4 d''8 c''8 b'8 a'8  | b'4    c''8 b'8 a'8 g'8 | fs'4 g'8  a'8  b'8  g'8   | \acciaccatura b'8 a'2. | \break
      
      d''4 g'8  a'8  b'8 c''8 | d''4-. g'4-.    g'4-.   | e''4 c''8 d''8 e''8 fs''8 | g''4-. g'4-. g'4-. | \break
      c''4 d''8 c''8 b'8 a'8  | b'4    c''8 b'8 a'8 g'8 | a'4  b'8  a'8  g'8  fs'8  | g'2.               | \break
      
      \B
      
      b''4    g''8  a''8 b''8 g''8  | a''4   d''8 e''8 fs''8 d''8 | g''4    e''8 fs''8 g''8 e''8 | cs''4 b'8 cs''8 a'4 | \break
      a'8 b'8 cs''8 d''8 e''8 fs''8 | g''4-. fs''4-.   e''4-.     | fs''4-. a'4-.      cs''4-.   | d''2.               | \break
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 3/4
      
      <g b d'>2 a4 | b2. | c'2.      | b2.              |
      a2.          | g2. | d'4 b4 g4 | d'4 d8 c'8 b8 a8 |
      
      b2 a4  | g4 b4 g4 | c'2.       | b4 c'8 b8 a8 g8 |
      a2 fs4 | g2    b4 | c'4 d'4 d4 | g2        g,4   |
      
      g2. | fs2.              | e4    g4    e4   | g2     a,4 |
      a2. | b4-. d'4-. cs'4-. | d'4-. fs4-. a4-. | d'4 d4 c'4 |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
