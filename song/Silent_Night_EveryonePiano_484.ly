\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Silent Night"
  tagline = "EveryonePiano 484"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

C      = { c4  e4 g4 }
F      = { c4  f4 a4 }
G      = { b,4 d4 g4 }
Gseven = { b,4 f4 g4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      g'4.^2 a'8 g'4  | e'2.^1 | g'4. a'8 g'4  | e'2. | \break
      d''2^5     d''4 | b'2.   | c''2^5   c''4 | g'2. | \break
      
      a'2    a'4  | c''4. b'8  a'4 | g'4. a'8 g'4 | e'2.^1 | \break
      a'2    a'4  | c''4. b'8  a'4 | g'4. a'8 g'4 | e'2.   | \break
      d''2^3 d''4 | f''4. d''8 b'4 | c''2.        | e''2.  | \break
      
      c''4^5 g'4^2 e'4^1 | g'4.^5 f'8 d'4 | c'2.~ | c'2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \C | \C | \C | \C |
      \G | \G | \C | \C |
      
      \F | \F | \C | \C |
      \F | \F | \C | \C |
      \G | \G | \C | \C |
      
      \C | \Gseven | \C | c2. |
    }
    \chords {
      c2. | c2. | c2. | c2. |
      g2. | g2. | c2. | c2. |
      
      f2. | f2. | c2. | c2. |
      f2. | f2. | c2. | c2. |
      g2. | g2. | c2. | c2. |
      
      c2. | g2.:7 | c2. | r2. |
    }
  >>
  \layout {}
  \midi {}
}
