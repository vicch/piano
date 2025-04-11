\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "The Blue Danube"
  tagline = "EveryonePiano 1681"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

C      = { c4  <<e4 g4>> <<e4 g4>> }
Gfive  = { d4  <<f4 g4>> <<f4 g4>> }
Gseven = { b,4 <<f4 g4>> <<f4 g4>> }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      c'4 e'4 g'4 | g'4 r4 <<e''4 g''4>> | <<e''4 g''4>> r4 <<c''4 e''4>> | <<c''4 e''4>> r4 c'4 | \break
      c'4 e'4 g'4 | g'4 r4 <<f''4 g''4>> | <<f''4 g''4>> r4 <<d''4 f''4>> | <<d''4 f''4>> r4 b4  | \break
      b4  d'4 a'4 | a'4 r4 <<f''4 a''4>> | <<f''4 a''4>> r4 <<d''4 f''4>> | <<d''4 f''4>> r4 b4  | \break
      b4  d'4 a'4 | a'4 r4 <<f''4 a''4>> | <<e''4 a''4>> r4 <<c''4 e''4>> | <<c''4 e''4>> r4 c'4 | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r2.     | \C     | \C     | \C      |
      \C      | \Gfive | \Gfive | \Gseven |
      \Gseven | \Gfive | \Gfive | \Gseven |
      \C      | \C     | \C     | \C      |
    }
    \chords {
      
      r2.   | c2.   | c2.   | c2.   |
      c2.   | g2.:5 | g2.:5 | g2.:7 |
      g2.:7 | g2.:5 | g2.:5 | g2.:7 |
      c2.   | c2.   | c2.   | c2.   |
    }
  >>
  \layout {}
  \midi {}
}
