\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "The End of the World"
  tagline = "EveryonePiano 5556"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

C      = { c8  g8  c'8 e'8  c'8 g8  }
Dm     = { d8  a8  d'8 f'8  d'8 a8  }
Em     = { e,8 b,8 e8  g8   e8  b,8 }
G      = { g,8 d8  g8  b8   g8  d8  }
Gseven = { g,8 g8  b8  f'8  b8  g8  }
A      = { a,8 e8  a8  cs'8 a8  e8  }
Am     = { a,8 e8  a8  c'8  a8  e8  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 6/8
      
      e''4.~ e''8 e''8 d''8 | c''4. e''4 a''8 | g''8 d''4.~ d''4~ | d''4. r4. | \break
      c''4.~ c''8 c''8 b'8  | a'4.  c''4 f''8 | e''2.~            | e''4. r4. | \break
      
      d''4. a''4 g''8 | a''4.~     a''8 g''8 a''8 | b''4. g''4 e''8 | g''4.~ g''4 e''8 | \break
      a''4. g''4.     | f''8 e''4~ e''8 d''8 e''8 | f''2.~          | f''4.  r4.       | \break
      
      e''4.~ e''8 e''8 d''8 | c''4. e''4 a''8 | g''8 d''4.~ d''4~ | d''4. r4. | \break
      c''4.~ c''8 c''8 b'8  | a'4.  c''4 f''8 | e''2.~            | e''4. r4. | \break
      
      d''4.      a''4 g''8 | a''4.~     a''8 g''8 a''8 | b''4. g''4 e''8 | g''4.~ g''4 e''8 | \break
      a''4  f''8 d''4 c''8 | b'4.       d''4.          | c''2.~          | c''4.  r4   c''8 | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 6/8
      
      \C  | \C  | \G  | \G  |
      \Am | \Am | \Em | \Em |
      
      \Dm | \Dm | \Em     | \A      |
      \Dm | \Dm | \Gseven | \Gseven |
      
      \C  | \C  | \G  | \G  |
      \Am | \Am | \Em | \Em |
      
      \Dm | \Dm     | \Em | \A |
      \Dm | \Gseven | \C  | \C |
    }
    \chords {
      c2.   | c2.   | g2.   | g2.   |
      a2.:m | a2.:m | e2.:m | e2.:m |
      
      d2.:m | d2.:m | e2.:m | a2.   |
      d2.:m | d2.:m | g2.:7 | g2.:7 |
      
      c2.   | c2.   | g2.   | g2.   |
      a2.:m | a2.:m | e2.:m | e2.:m |
      
      d2.:m | d2.:m | e2.:m | a2. |
      d2.:m | g2.:7 | c2.   | c2. |
    }
  >>
  \layout {}
  \midi {}
}
