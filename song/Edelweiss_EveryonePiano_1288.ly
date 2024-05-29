\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Edelweiss"
  tagline = "EveryonePiano 1288"
}

\markup \vspace #1.5

chordds    = { bf,4 ef4 g4 }
chordf     = { a,4  c4  f4 }
chordas    = { bf,4 d4  f4 }
chordassix = { bf,4 d4  g4 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key bf \major
      \time 3/4
      
      d'2            f'4 | c''2.       | bf'2 f'4 | ef'2. | d'2 d'4  | d'4  ef'4 f'4  | g'2.  | f'2.          | \break
      d'2            f'4 | c''2.       | bf'2 f'4 | ef'2. | d'2 f'4  | f'4  g'4  a'4  | bf'2. | bf'2.         | \break
      c''8 r8 r8 f'8 f'4 | a'4 g'4 f'4 | d'2  f'4 | bf'2. | g'2 bf'4 | c''2      bf'4 | a'2.  | f'2.          | \break
      d'2            f'4 | c''2.       | bf'2 f'4 | ef'2. | d'2 f'4  | f'4  g'4  a'4  | bf'2. | bf'2.\fermata | \bar "|."
    }
    \new Staff {
      \clef bass
      \key bf \major
      \time 3/4
      
      \chordas | \chordf | \chordas | \chordds | \chordas | f4 ef4 d4 | \chordds | \chordas                  |
      \chordas | \chordf | \chordas | \chordds | \chordas | f4 ef4 d4 | \chordas | \chordas                  |
      \chordf  | \chordf | \chordas | \chordas | \chordds | \chordf   | \chordf  | \chordassix               |
      \chordas | \chordf | \chordas | \chordds | \chordas | f4 ef4 d4 | \chordas | bf,4 d4 <<d4 f4\fermata>> |
    }
    \chords {
      \set noChordSymbol = ""
      
      as2. | f2. | as2. | ds2. | as2. | r2. | ds2. | as2.   |
      as2. | f2. | as2. | ds2. | as2. | r2. | as2. | as2.   |
      f2.  | f2. | as2. | as2. | ds2. | f2. | f2.  | as2.:6 |
      as2. | f2. | as2. | ds2. | as2. | r2. | as2. | as2.   |
    }
  >>
  \layout {}
  \midi {}
}
