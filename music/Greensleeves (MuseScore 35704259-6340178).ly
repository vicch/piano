\version "2.24.3"

#(define title      "Greensleeves")
#(define title-font "")
#(define sequence   "MuseScore 35704259-6340178")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

"C135"   = { c4  e4   g4  }
"E135-2" = { e,4 gs,4 b,4 }
"E135-3" = { e4  gs4  b4  }
"F135-2" = { f,4 a,4  c4  }
"F135-3" = { f4  a4   c'4 }
"G135-2" = { g,4 b,4  d4  }
"G135-3" = { g4  b4   d'4 }

"A13b5-2" = { a,4 c4  e4  }
"A13b5-3" = { a4  c'4 e'4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      \partial 4 a'4 | c''2     d''4 | e''4.       f''8 e''4       | d''2 b'4 | g'4. a'8 b'4                      | c''2           a'4 | a'4.  gs'8 a'4  | b'2 gs'4 |        \break
      e'2        a'4 | <a'c''>2 d''4 | <c'' e''>4. f''8 <e'' g''>4 | d''2 b'4 | g'4. r8  \tuplet 3/2 { g' a' b' } | <a' c''>4. b'8 a'4 | gs'4. fs'8 gs'4 | a'2.~    | a'2. | \break
      
      g''2.      | g''4.        fs''8 e''4 | d''2 b'4 | g'4. a'8 b'4                      | c''2            a'4 | a'4.       gs'8 a'4  | b'2 gs'4 | e'2. | \break
      <c''g''>2. | <e'' g''> 4. fs''8 e''4 | d''2 b'4 | g'4. r8  \tuplet 3/2 { g' a' b' } | <a' c''> 4. b'8 a'4 | <e' gs'>4. fs'8 gs'4 | a'2.~    | a'2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r4        | \"A13b5-2" | \"A13b5-2" | \"G135-2" | \"G135-2" | \"F135-2" | \"F135-2" | \"E135-2"  |
      \"E135-2" | \"A13b5-2" | \"C135"    | \"G135-2" | \"G135-2" | \"F135-2" | \"E135-2" | \"A13b5-2" | a,2. |
      
      \"C135" | \"C135"   | \"G135-3" | \"G135-3" | \"F135-3" | \"F135-3" | \"E135-3"  | \"E135-3" |
      \"C135" | c'4 b4 a4 | \"G135-3" | \"G135-3" | \"F135-3" | \"E135-3" | \"A13b5-3" | a2.       |
    }
    \chords {
      r4  | a2.:m | a2.:m | g2. | g2. | f2. | f2. | e2.   |
      e2. | a2.:m | c2.   | g2. | g2. | f2. | e2. | a2.:m | r2. |
      
      c2. | c2. | g2. | g2. | f2. | f2. | e2.   | e2. |
      c2. | r2. | g2. | g2. | f2. | e2. | a2.:m | r2. |
    }
  >>
  \layout {}
  \midi {}
}
