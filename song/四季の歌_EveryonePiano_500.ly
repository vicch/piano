\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "四季の歌"
  tagline = "EveryonePiano 500"
}

\markup \vspace #1.25

Aseven = { cs8 g8 a4    }
Dmi    = { d8  f8 a4    }
Dmii   = { d8  f8 a8 f8 }
Gm     = { d8  g8 bf4   }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 4/4
      
      a'4^5  a'8^5  g'8^4 f'8^3 g'8^4 f'8^3 e'8^2  | d'4^1 d'4         d'2       | bf'4^4 bf'8^4 a'8^3 g'8^2 f'8^1 g'8^2 bf'8^4 | a'1^3 | \break
      bf'4^4 bf'8^4 a'8^3 g'4^2       g'8^2 bf'8^4 | a'4^3 a'8^3 f'8^2 d'4^1 d'4 | e'4^2  a'8^5  a'8   g'8^4 f'8^3 e'8^2 f'8^3  | d'1^1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 4/4
      
      \Dmi \Dmi | \Dmii d8^5 f8^3 g8^2 a8^1 | \Gm     \Gm     | \Dmii d8^5 e8^4 f8^3 a8^1 |
      \Gm  \Gm  | \Dmi  \Dmii               | \Aseven \Aseven | \Dmii d2                  |
    }
    \chords {
      \set noChordSymbol = ""
      
      d1:m | d1:m | g1:m | d1:m |
      d1:m | d1:m | a1:7 | d1:m |
    }
  >>
  \layout {}
  \midi {}
}
