\version "2.24.3"

#(define title      "Home Sweet Home")
#(define title-font "")
#(define sequence   "EveryonePiano 535")
#(define total-page 1)

\include "../base.ly"

\paper {
  ragged-last = ##t
}

\markup \vspace #1.5

CI         = { e8 g8  c'8 g8  }
CsevensusI = { c8 g8  bf8 g8  }
FI         = { f8 a8  c'8 a8  }
FII        = { c8 f8  a8  f8  }
GmI        = { d8 g8  bf8 g8  }
AmI        = { c8 a8  c'8 a8  }
AsI        = { f8 bf8 d'8 bf8 }
AsII       = { d8 f8  bf8 f8  }

FIII = { f8 c8 a,8 c8 f,2 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 4/4
      
      \partial 4 f'8 g'8 | a'4. bf'8 bf'4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      a'2.       f'8 g'8 | a'4. bf'8 bf'4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      
      f'2. c''8 c''8 | f''4. e''8 d''4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      a'2. c''8 c''8 | f''4. e''8 d''4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      
      f'1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 4/4
       
          r4   | \FI \CI | \FI \FI | \CI \CsevensusI |
      \FI \AmI | \FI \CI | \FI \FI | \CI \CsevensusI |
      
      \FIII             | \AsI  e8 bf8 c'8 bf8 | \FI  \FI  | \CI  \CsevensusI |
      \FI ef8 a8 c'8 a8 | \AsII c8 f8  bf8 f8  | \FII \FII | \GmI \CsevensusI |
      
      \FIII |
    }
    \chords {
         r4   | f2 c2 | f2 f2 | c2 c2:7sus4 |
      f2 a2:m | f2 c2 | f2 f2 | c2 c2:7sus4 |
      
      f1    | as2 r2 | f2 f2 | c2   c2:7sus4 |
      f2 r2 | as2 r2 | f2 f2 | g2:m c2:7sus4 |
      
      f1 |
    }
  >>
  \layout {}
  \midi {}
}
