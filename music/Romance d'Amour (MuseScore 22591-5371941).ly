\version "2.24.3"

#(define title      "Romance d'Amour")
#(define title-font "")
#(define sequence   "MuseScore 22591-5371941")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

"EBG4" = { \tuplet 3/2 { e'8  b8  g8  } }
"EBG5" = { \tuplet 3/2 { e''8 b'8 g'8 } }
"FBG"  = { \tuplet 3/2 { fs'8 b8  g8  } }
"GBG"  = { \tuplet 3/2 { g'8  b8  g8  } }

"GEB" = { \tuplet 3/2 { g'8 e'8 b8 } }
"AEB" = { \tuplet 3/2 { a'8 e'8 b8 } }
"BEB" = { \tuplet 3/2 { b'8 e'8 b8 } }

"CGE" = { \tuplet 3/2 { c''8 g'8 e'8 } }
"DGE" = { \tuplet 3/2 { d''8 g'8 e'8 } }
"BGE" = { \tuplet 3/2 { b'8  g'8 e'8 } }

"CEC" = { \tuplet 3/2 { c''8 e'8 c'8 } }
"AEC" = { \tuplet 3/2 { a'8  e'8 c'8 } }
"BEC" = { \tuplet 3/2 { b'8  e'8 c'8 } }

"CFD" = { \tuplet 3/2 { c''8  fs'8 ds'8 } }
"DFD" = { \tuplet 3/2 { ds''8 fs'8 ds'8 } }
"BFD" = { \tuplet 3/2 { b'8   fs'8 ds'8 } }

"FBA" = { \tuplet 3/2 { fs'8 b8 a8 } }
"GBA" = { \tuplet 3/2 { g'8  b8 a8 } }

"E158"  = { e,4  b,4 e4 }
"A158"  = { a,4  e4  a4 }
"B158"  = { b,4  fs4 b4 }
"B,158" = { b,,4 fs4 b4 }

"B135"  = { b,4  ds4 fs4 }
"B,135" = { b,,4 ds4 fs4 }

"Eb351" = { g,4 b,4 e4  }
"E15b3" = { e4  b,4 g,4 }
"Ab351" = { c4  e4  a4  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key g \major
      \time 3/4
      
      \repeat volta 2 {
        \"BGE"  \"BGE"  \"BGE"  | \"BGE"  \"AEB" \"GEB" | \"GBG"  \"FBG"  \"EBG4" | \"EBG4" \"GEB" \"BGE"  | \break
        \"EBG5" \"EBG5" \"EBG5" | \"EBG5" \"DGE" \"CGE" | \"CEC"  \"BEC"  \"AEC"  | \"AEC"  \"BEC" \"CEC"  | \break
        \"BFD"  \"CFD"  \"BFD"  | \"DFD"  \"CFD" \"BFD" | \"BEB"  \"AEB"  \"GEB"  | \"GBG"  \"FBG" \"EBG4" | \break
        \"FBA"  \"FBA"  \"FBA"  | \"FBA"  \"GBA" \"FBA" | \"EBG4" \"EBG4" \"EBG4" | e'2.                   | \break
      }
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 3/4
      
      \"E158" | \"E158"  | \"E158"  | \"E158"  |
      \"E158" | \"E158"  | \"A158"  | \"Ab351" |
      \"B158" | \"B,158" | \"E158"  | \"Eb351" |
      \"B135" | \"B,135" | \"E15b3" | e,2.     |
    }
    \chords {
      e2. | e2. | e2.   | e2.   |
      e2. | e2. | a2.   | a2.:m |
      b2. | b2. | e2.   | e2.:m |
      b2. | b2. | e2.:m | r2.   |
    }
  >>
  \layout {}
  \midi {}
}
