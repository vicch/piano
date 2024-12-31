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

Fsfive = { fs,,8 cs,8 fs,8 gs,8 as,2 }
Fseven = { es,,8 gss,,8 bs,,8 ds,8 es,2 }
Gfive  = { gs,,8 ds,8 gs,8 as,8 bs,2 }
Asfive = { as,,8 es,8 as,8 bs,8 cs2  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key cs \major
      \time 4/4
      
      \partial 4 cs'8 ds'8 | es'2. es'8 as8 | es'2. es'8 cs'8 | ds'2. es'8 es'8 | as2. \break
    }
    \new Staff {
      \clef bass
      \key cs \major
      \time 4/4
      
      r4 | \Asfive | \Gfive | \Fsfive | \Fseven |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
