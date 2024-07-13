\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Romance d'Amour"
  tagline = "EveryonePiano 1704"
}

\markup \vspace #1.5

A  = { a,8 e8  a8 e8  cs'4 }
Am = { a,8 e8  a8 e8  c'4  }
Dm = { d,8 a,8 d8 a,8 f4   }
E  = { e,8 b,8 e8 b,8 gs4  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      e''4 e''4 e''4 | e''4  d''4 c''4 | c''4 b'4  a'4  | a'4  c''4 e''4 | \break
      a''4 a''4 a''4 | a''4  g''4 f''4 | f''4 e''4 d''4 | d''4 e''4 f''4 | \break
      e''4 f''4 e''4 | gs''4 f''4 e''4 | e''4 d''4 c''4 | c''4 b'4  a'4  | \break
      b'4  b'4  b'4  | b'4   c''4 b'4  | a'4  a'4  a'4  | \acciaccatura a'8 <a' a''>2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \magnifyMusic 1 {
        \Am | \Am | \Am | \Am |
        \A  | \A  | \Dm | \Dm |
        \E  | \E  | \Am | \Am |
        \E  | \E  | \Am | <a, e a>2. |
      }
    }
    \chords {
      \set noChordSymbol = ""
      
      a2.:m | a2.:m | a2.:m | a2.:m |
      a2.   | a2.   | d2.:m | d2.:m |
      e2.   | e2.   | a2.:m | a2.:m |
      e2.   | e2.   | a2.:m | a2.:m |
    }
  >>
  \layout {}
  \midi {}
}