\version "2.24.3"

#(define title      "パリは燃えているか")
#(define title-font "FangSong")
#(define sequence   "MuseScore 79422415-14370538")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

"Df135"   = { << { r8 <af, f>4 <af, f>4 <af, f>4 <af, f>8 } \\ { df,1 } >> }
"Ef135"   = { << { r8 <bf, g>4 <bf, g>4 <bf, g>4 <bf, g>8 } \\ { ef,1 } >> }
"F1m35"   = { << { r8 <c af>4  <c af>4  <c af>4  <c af>8  } \\ { f,1  } >> } 
"Bf1m35"  = { << { r8 <f df'>4 <f df'>4 <f df'>4 <f df'>8 } \\ { bf,1 } >> }
"Bf1m345" = { << { r8 <f df'>4 <f df'>4 <f ef'>4 <f ef'>8 } \\ { bf,1 } >> }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key af \major
      \time 4/4
      
      <bf' df''>1 | <g'  bf'>1            | <af' c''>1~ | <af' c''>1 | \break
      <c'' ef''>1 | <bf' df''>2 <g' bf'>2 | <af' c''>1~ | <af' c''>1 | \break
      <f'  bf'>1  | <df' f'>1             | <ef' g'>1   | <bf  ef'>1 | \break
    }
    \new Staff {
      \clef bass
      \key af \major
      \time 4/4
      
      \"Bf1m35" | \"Bf1m35"  | \"F1m35" | \"F1m35" |
      \"Bf1m35" | \"Bf1m345" | \"F1m35" | \"F1m35" |
      \"Df135"  | \"Df135"   | \"Ef135" | \"Ef135" |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
