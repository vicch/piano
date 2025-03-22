\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Home! Sweet Home!"
  tagline = "EveryonePiano 535"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

C  = { e8 g8 c'8 g8 }
F  = { f8 a8 c'8 a8 }
Am = { c8 a8 c'8 a8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 4/4
      
      \partial 4 f'8 g'8 | a'4. bf'8 bf'4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | a'2. f'8  g'8  | \break
                         | a'4. bf'8 bf'4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | f'2. c''8 c''8 | \break
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 4/4
      
      r4 | \F \C | \F \F | \C c8 g8 bf8 g8 | \F           \Am |
         | \F \C | \F \F | \C c8 g8 bf8 g8 | f8 c8 a,8 c8 f,2 |
    }
    \chords {
      
      r4 | f2 c2 | f2 f2 | c2 r2 | f2 a2:m |
         | f2 c2 | f2 f2 | c2 r2 | r1      |
    }
  >>
  \layout {}
  \midi {}
}
