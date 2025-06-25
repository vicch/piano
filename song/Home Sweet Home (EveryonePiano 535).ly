\version "2.24.3"

#(define title      "Home Sweet Home")
#(define title-font "")
#(define sequence   "EveryonePiano 535")
#(define total-page 1)

\include "../base.ly"

\page {
  ragged-last = ##t
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
      
      \partial 4 f'8  g'8  | a'4.  bf'8 bf'4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      a'2.       f'8  g'8  | a'4.  bf'8 bf'4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      f'2.       c''8 c''8 | f''4. e''8 d''4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      a'2.       c''8 c''8 | f''4. e''8 d''4 c''4 | c''2 a'4 c''4 | bf'4. a'8 bf'4 g'4 | \break
      f'2.       r4        | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 4/4
       
                   r4  | \F             \C             | \F \F | \C c8 g8 bf8 g8 |
      \F           \Am | \F             \C             | \F \F | \C c8 g8 bf8 g8 |
      f8 c8 a,8 c8 f,2 | f8 bf8 d'8 bf8 e8 bf8 c'8 bf8 | \F \F | \C c8 g8 bf8 g8 |
      \F           
    }
    \chords {
      
         r4   | f2 c2 | f2 f2 | c2 r2 |
      f2 a2:m | f2 c2 | f2 f2 | c2 r2 |
      r1      | r1    | f2 f2 | c2 r2 |
    }
  >>
  \layout {}
  \midi {}
}
