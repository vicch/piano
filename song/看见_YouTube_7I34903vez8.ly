\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "看见"
  tagline = "YouTube 7I34903vez8"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

CsMaj = { as,8 es8 as8 bs8 cs'2 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key cs \major
      \time 4/4  
                           
      \partial 4 cs''8 ds''8 | es''2.             es''8 as'8 | es''2. es''8 cs''8 | ds''2~ ds''8 es''8 es''4 | bs'2. cs''8 ds''8 \break
                             | es''2~ es''8 es''8 es''8 as'8 | es''2. es''8 cs''8 | ds''2~ ds''8 gs''8 cs''4 | bs'1              \break
                             
                             | as'8 bs'8 cs''8 gs''8 g''4  ds''4 | es''1 | as'8  bs'8  cs''8 gs''8 fs''4 ds''4       | es''1 | \break
                             | as'8 bs'8 cs''8 gs''8 fs''4 ds''4 | es''1 | cs''8 ds''8 es''2~            es''8 es''8 | es''1 | \break
    }
    \new Staff {
      \clef bass
      \key cs \major
      \time 4/4
      
      r4 | \CsMaj |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
