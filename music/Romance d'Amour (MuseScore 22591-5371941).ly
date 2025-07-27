\version "2.24.3"

#(define title      "Romance d'Amour")
#(define title-font "")
#(define sequence   "MuseScore 22591-5371941")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

"EBG4" = { \tuplet 3/2 { e'8  b  g  } }
"EBG5" = { \tuplet 3/2 { e'' b' g' } }
"FBG"  = { \tuplet 3/2 { fs' b  g  } }
"GBG"  = { \tuplet 3/2 { g'  b  g  } }

"EBGs"  = { \tuplet 3/2 { e'   b  gs } }
"FsBGs" = { \tuplet 3/2 { fs'  b  gs } }
"GsBGs" = { \tuplet 3/2 { gs'  b  gs } }

"GEB" = { \tuplet 3/2 { g' e' b } }
"AEB" = { \tuplet 3/2 { a' e' b } }
"BEB" = { \tuplet 3/2 { b' e' b } }

"CGE" = { \tuplet 3/2 { c'' g' e' } }
"DGE" = { \tuplet 3/2 { d'' g' e' } }
"BGE" = { \tuplet 3/2 { b'  g' e' } }

"CEC" = { \tuplet 3/2 { c'' e' c' } }
"AEC" = { \tuplet 3/2 { a'  e' c' } }
"BEC" = { \tuplet 3/2 { b'  e' c' } }

"CFD" = { \tuplet 3/2 { c''  fs' ds' } }
"DFD" = { \tuplet 3/2 { ds'' fs' ds' } }
"BFD" = { \tuplet 3/2 { b'   fs' ds' } }

"FBA" = { \tuplet 3/2 { fs' b a } }
"GBA" = { \tuplet 3/2 { g'  b a } }

"DAFs"  = { \tuplet 3/2 { d'  a fs } }
"DsAFs" = { \tuplet 3/2 { ds' a fs } }
"EAFs"  = { \tuplet 3/2 { e'  a fs } }

"E158"  = { e,4  b,4 e4 }
"A158"  = { a,4  e4  a4 }
"B158-1" = { b,4  fs4  b4  }
"B158-2" = { b,,4 fs4  b4  }
"B158-3" = { b,,4 fs,4 b,4 }

"B135"  = { b,4  ds4 fs4 }
"B,135" = { b,,4 ds4 fs4 }
"B513"  = { fs,4 b,4 ds4 }

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
      
      \repeat volta 2 {
        \key e \major
        
        \"GsBGs" \"GsBGs" \"GsBGs" | \"GsBGs" \"FsBGs" \"EBGs" | \"EAFs" \"DsAFs" \"DsAFs" | \"DsAFs" \"DAFs" \"DsAFs" | \break
      }
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 3/4
      
      \"E158"   | \"E158"   | \"E158"  | \"E158"  |
      \"E158"   | \"E158"   | \"A158"  | \"Ab351" |
      \"B158-1" | \"B158-2" | \"E158"  | \"Eb351" |
      \"B135"   | \"B,135"  | \"E15b3" | e,2.     |
      
      \key e \major
      \"E158" | \"E158" | \"B513" | \"B158-3" |
    }
    \chords {
      e2. | e2. | e2.   | e2.   |
      e2. | e2. | a2.   | a2.:m |
      b2. | b2. | e2.   | e2.:m |
      b2. | b2. | e2.:m | r2.   |
      
      e2. | e2. | b2. | b2. |
    }
  >>
  \layout {}
  \midi {}
}
