\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "洋娃娃和小熊跳舞"
  tagline = "EveryonePiano 505"
}

\paper {
  total-page = 1
}

\markup \vspace #1.25

C      = { e8^.[ c'8^. g8^.  c'8^.] }
Cseven = { e8^.[ c'8^. bf8^. c'8^.] }
F      = { f8^.[ c'8^. a8^.  c'8^.] }
As     = { f8^.[ d'8^. bf8^. d'8^.] }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 2/4
      
      f'8^1[  g'8^2 a'8^3           bf'8^4] | c''8^5 c''8 c''16^5 bf'16^4 a'8^3 | bf'8^4 bf'8 bf'16^4 a'16^3 g'8^2 | f'8^1 a'8^3 c''4^5 | \break
      f'8[    g'8   a'8             bf'8]   | c''8   c''8 c''16   bf'16   a'8   | bf'8   bf'8 bf'16 a'16   g'8     | f'8^1 a'8^3 f'4^1  | \break
      d''8^5  d''8  d''16^5 c''16^4 bf'8^3  | c''8^5 c''8 c''16^5 bf'16^4 a'8^3 | bf'8^4 bf'8 bf'16^4 a'16^3 g'8^2 | f'8 a'8 c''4       | \break
      d''8    d''8  d''16   c''16   bf'8    | c''8   c''8 c''16   bf'16   a'8   | bf'8   bf'8 bf'16   a'16   g'8   | f'8 a'8 f'4        | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 2/4
      
      \F  | \F | \C      | \F |
      \F  | \F | \C      | \F |
      \As | \F | \C      | \F |
      \As | \F | \Cseven | f8^. <<a8 c'8^.>> <<a4 c'4^.>> |
    }
    \chords {
      f2  | f2 | c2   | f2 |
      f2  | f2 | c2   | f2 |
      as2 | f2 | c2   | f2 |
      as2 | f2 | c2:7 | f2 |
    }
  >>
  \layout {}
  \midi {}
}

