\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Twinkle Twinkle Little Star"
  tagline = "EveryonePiano 1656"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

C = { c8  g8 e8 g8 }
F = { c8  a8 f8 a8 }
G = { b,8 g8 d8 g8 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 4/4
      
      c'4^1 c'4 g'4^4 g'4 | a'4^5 a'4 g'2^4 | f'4^4 f'4 e'4^3 e'4 | d'4^2 d'4 c'2^1 | \break
      g'4^5 g'4 f'4^4 f'4 | e'4^3 e'4 d'2^2 | g'4   g'4 f'4   f'4 | e'4   e'4 d'2   | \break
      c'4   c'4 g'4   g'4 | a'4   a'4 g'2   | f'4   f'4 e'4   e'4 | d'4   d'4 c'2   | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \C \C | \F \C | \G \C | \G \C       |
      \C \G | \C \G | \C \G | \C \G       |
      \C \C | \F \C | \G \C | \G <c e g>2 |
    }
    \chords {
      c2 c2 | f2 c2 | g2 c2 | g2 c2 |
      c2 g2 | c2 g2 | c2 g2 | c2 g2 |
      c2 c2 | f2 c2 | g2 c2 | g2 c2 |
    }
  >>
  \layout {}
  \midi {}
}
