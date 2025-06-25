\version "2.24.3"

#(define title      "春天在哪里")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 556")
#(define total-page 2)

\include "../base.ly"

\markup \vspace #1.5

Ci    = { e8 <<g8  c'8>> c8          <<g8  c'8>> }
Cii   = { c8 <<g8  c'8>> e8          <<g8  c'8>> }
Ciii  = { e8 <<g8  c'8>> <<g8  c'8>> <<g8  c'8>> }
Fi    = { f8 <<a8  c'8>> <<a8  c'8>> <<a8  c'8>> }
Fii   = { f8 <<a8  c'8>> c8          <<a8  c'8>> }
As    = { f8 <<bf8 d'8>> <<bf8 d'8>> <<bf8 d'8>> }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 2/4
      
      a''8  a''8  a''8  f''8  | c''4        c''4      | a''8 a''8 a''8 f''8 | a''4      r4 | \break
      c'''8 c'''8 a''8  f''8  | c''8  c''8  c''4      | d''8 e''8 f''8 a''8 | g''4      r4 | \break
      a''8  a''8  a''8  f''8  | c''4        c''4      | a''8 a''8 a''8 f''8 | a''4      r4 | \break
      c'''8 d'''8 c'''8 d'''8 | c'''8 bf''8 a''8 f''8 | c''4      a''4      | g''8 f''8 r4 | \break
      
      bf''8 bf''8 bf''8 c'''8 | d'''8 d'''8 d'''4 | g''8 g''8 g''8 g''8 | c'''2 | \break \pageBreak
      f''8  f''8  f''8  g''8  | a''8  a''8  a''4  | c''8 c''8 c''8 c''8 | g''2  | \break
      
      c'''8 d'''8 c'''8 d'''8 | c'''8 bf''8 a''8 f''8 | g''4 c''4 | f''8 a''8 r4 | \break
      c'''8 d'''8 c'''8 d'''8 | c'''8 bf''8 a''8 f''8 | c''4 a''4 | g''8 f''8 r4 | <a'' c''' f'''>4 r4 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 2/4
      
      \Fi | \Fii | \Fi  | \Fii                |
      \Fi | \Fii | \As  | \Ci                 |
      \Fi | \Fii | \Fi  | \Fii                |
      \Fi | \Fii | \Cii | f8 <<a8 c'8>> g8 a8 |
      
      \As | \As | \Ciii | \Ciii |
      \Fi | \Fi | \Ciii | \Ciii |
      
      \Fii | \Fii | \Cii | \Fii |
      \Fii | \Fii | \Cii | \Fii | <<f4 a4>> r4 |
    }
    \chords {
      
      f2 | f2 | f2  | f2    |
      f2 | f2 | as2 | c2    |
      f2 | f2 | f2  | f2    |
      f2 | f2 | c2  | f4 r4 |
      
      as2 | as2 | c2 | c2 |
      f2  | f2  | c2 | c2 |
      
      f2 | f2 | c2 | f2 |
      f2 | f2 | c2 | f2 | r2 |
    }
  >>
  \layout {}
  \midi {}
}
