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

FI  = { fs,8 cs8   fs8  gs8 as2  }
FII = { es,8 gss,8 bs,8 ds8 es2  }
GI  = { gs,8 ds8   gs8  as8 bs2  }
AI  = { as,8 es8   as8  bs8 cs'2 }

FIII = { fs,8 cs8   fs4 }
DI   = { ds,8 fss,8 ds4 }
DII  = { ds,8 as,8  ds4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key cs \major
      \time 4/4
      
      r2.   cs''8 ds''8 | es''2.             es''8 as'8 | es''2. es''8 cs''8 | ds''2~ ds''8 es''8 es''4 | \break
      bs'2. cs''8 ds''8 | es''2~ es''8 es''8 es''8 as'8 | es''2. es''8 cs''8 | ds''2~ ds''8 gs''8 cs''4 | bs'1 | \break
      
      as'8 bs'8 cs''8 gs''8 fss''4 ds''4 | es''1 | as'8  bs'8  cs''8 gs''8 fs''4 ds''4       | es''1 | \break
      as'8 bs'8 cs''8 gs''8 fs''4  ds''4 | es''1 | cs''8 ds''8 es''2~            es''8 es''8 | es''1 | \break
    }
    \new Staff {
      \clef bass
      \key cs \major
      \time 4/4
      
      r1   | \AI | \GI | \FI |
      \FII | \AI | \GI | \FI | \FII |
      
      \FIII \DI | \FII | \FIII \DII | \FII |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
