\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Edelweiss"
  tagline = "EveryonePiano 1288"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

Ds    = { bf,4 ef4 g4 }
F     = { a,4  c4  f4 }
As    = { bf,4 d4  f4 }
Assix = { bf,4 d4  g4 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key bf \major
      \time 3/4
      
      d'2^1              f'4^2 | c''2.^5           | bf'2^5 f'4^3 | ef'2.^2 | d'2^1 d'4    | d'4^1  ef'4^2 f'4^3  | g'2.^4  | f'2.^3        | \break
      d'2                f'4   | c''2.             | bf'2   f'4   | ef'2.   | d'2^1 f'4^2  | f'4^2  g'4^3  a'4^4  | bf'2.^5 | bf'2.         | \break
      c''8^5 r8 r8 f'8^2 f'4   | a'4^4 g'4^3 f'4^2 | d'2^1  f'4^2 | bf'2.^4 | g'2^2 bf'4^4 | c''2^5        bf'4^4 | a'2.^3  | f'2.^1        | \break
      d'2                f'4   | c''2.             | bf'2   f'4   | ef'2.   | d'2   f'4    | f'4    g'4    a'4    | bf'2.   | bf'2.\fermata | \bar "|."
    }
    \new Staff {
      \clef bass
      \key bf \major
      \time 3/4
      
      \As | \F | \As | \Ds | \As | f4 ef4 d4 | \Ds | \As                       |
      \As | \F | \As | \Ds | \As | f4 ef4 d4 | \As | \As                       |
      \F  | \F | \As | \As | \Ds | \F        | \F  | \Assix                    |
      \As | \F | \As | \Ds | \As | f4 ef4 d4 | \As | bf,4 d4 <<d4 f4\fermata>> |
    }
    \chords {
      as2. | f2. | as2. | ds2. | as2. | r2. | ds2. | as2.   |
      as2. | f2. | as2. | ds2. | as2. | r2. | as2. | as2.   |
      f2.  | f2. | as2. | as2. | ds2. | f2. | f2.  | as2.:6 |
      as2. | f2. | as2. | ds2. | as2. | r2. | as2. | as2.   |
    }
  >>
  \layout {}
  \midi {}
}
