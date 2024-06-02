\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "茉莉花"
  tagline = "EveryonePiano 518"
}

\markup \vspace #1.5

Cfive   = { c8  g8  c'8 g8  }
Dfive   = { d8  a8  d'8 a8  }
Dseven  = { d8  fs8 a8  c'8 }
Efive   = { e8  b8  e'8 b8  }
FfiveI  = { f8  c'8 f'8 c'8 }
FfiveII = { f,8 c8  f8  c8  }
GfiveI  = { g8  d'8 g'8 d'8 }
GfiveII = { g,8 d8  g8  d8  }
Afive   = { a,8 e8  a8  e8  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      e''4       e''8 g''8 a''8 c'''8 c'''8 a''8 | g''4 g''8 a''8  g''2         | e''4  e''8 g''8 a''8 c'''8 c'''8 a''8 | g''4 g''8 a''8 g''2                     | \break
      g''4       g''4      g''4       e''8  g''8 | a''4 a''4       g''2         | e''4  d''8 e''8 g''4       e''8  d''8 | c''4 c''8 d''8 c''2                     | \break
      e''8  d''8 c''8 e''8 d''4.            e''8 | g''4 a''8 c'''8 g''2         | d''4  e''8 g''8 d''8 e''8  c''8  a'8  | g'2            a'4 a'8  c''8            | \break
      d''4.           e''8 c''8 d''8  c''8  a'8  | g'2             a'4 a'8 c''8 | d''4.      e''8 c''8 d''8  c''8  a'8  | g''2          <b'' d''' g'''>2\arpeggio | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \Cfive   \Cfive   | \Cfive   \Cfive   | \Cfive   \Cfive  | \Cfive   c8 g8 c8 d8 |
      \Efive   \Efive   | \FfiveI  \GfiveI  | \Cfive   \Cfive  | \Afive   \Afive      |
      \Cfive   \Dfive   | \Efive   \Efive   | \Dfive   \Dfive  | \GfiveII \FfiveII    |
      \GfiveII \FfiveII | \GfiveII \FfiveII | \GfiveII \Dseven | g,8 g8 c'8 d'8 g'2   |
    }
    \chords {
      \set noChordSymbol = ""
      
      c1:5      | c1:5      | c1:5      | c2:5 r2   |
      e1:5      | f2:5 g2:5 | c1:5      | a1:5      |
      c2:5 d2:5 | e1:5      | d1:5      | g2:5 f2:5 |
      g2:5 f2:5 | g2:5 f2:5 | g2:5 d2:7 | r1        |
    }
  >>
  \layout {}
  \midi {}
}
