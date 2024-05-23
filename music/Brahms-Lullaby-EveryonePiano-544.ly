\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Brahms' Lullaby"
  tagline = "EveryonePiano 544"
}

\markup \vspace #1.5

chordc       = { c8[ g8]  c'8[ g8]  c'8[ g8]  }
chordcseven  = { c8[ g8]  bf8[ g8]  bf8[ g8]  }
chordcseveng = { g8[ bf8] c'8[ bf8] c'8[ bf8] }
chordfi      = { f8[ a8]  c'8[ a8]  c'8[ a8]  }
chordfii     = { f8[ a8]  c'8[ a8]  f4        }
chordas      = { f8[ bf8] d'8[ bf8] d'8[ bf8] }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 3/4
      
      \partial 4 a'8 a'8 | c''4. a'8     a'4       | c''2         a'8 c''8 | f''4             e''4. d''8 | d''4      c''4  \bar "" \break
                 g'8 a'8 | bf'4  g'4     g'8  a'8  | bf'2         g'8 bf'8 | e''8 d''8        c''4  e''4 | f''2            \bar "" \break
                 f'8 f'8 | <<d''2 f''2>> d''8 bf'8 | <<a'2 c''2>> a'8 f'8  | bf'4             c''4  d''4 | a'8 c''8( c''4) \bar "" \break
                 f'8 f'8 | <<d''2 f''2>> d''8 bf'8 | <<a'2 c''2>> a'8 f'8  | bf'8 c''16 bf'16 a'4   g'4  | f'2.            \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 3/4
      
      r4 | \chordfi      | \chordfi      | \chordas     | \chordfi
         | \chordcseveng | \chordcseveng | \chordcseven | \chordfii
         | \chordas      | \chordfi      | \chordc      | \chordfi
         | \chordas      | \chordfi      | \chordcseven | \chordfii
    }
    \chords {
      \set noChordSymbol = ""
      
      r4 | f2.   | f2.   | as2.  | f2.
         | c2.:7 | c2.:7 | c2.:7 | f2.
         | as2.  | f2.   | c2.   | f2.
         | as2.  | f2.   | c2.:7 | f2.
    }
  >>
  \layout {}
  \midi {}
}
