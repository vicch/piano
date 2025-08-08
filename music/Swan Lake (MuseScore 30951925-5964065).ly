\version "2.24.3"

#(define title      "Swan Lake")
#(define title-font "")
#(define sequence   "MuseScore 30951925-5964065")
#(define total-page 2)

\include "../base.ly"

\markup \vspace #1.5

"C135"  = { c8  e8   g8   e8   }
"Cs135" = { cs8 f8   gs8  f8   }
"Fs135" = { fs8 as8  cs'8 as8  }
"A135"  = { a8  cs'8 e'8  cs'8 }

"E1m35"  = { e8  g8  b8   g8  }
"Fs1m35" = { fs8 a8  cs'8 a8  }
"B1m35"  = { b8  d'8 fs'8 d'8 }

"E51m3" = { b8 e'8 g'8 e'8 }

"Em361" = { g8 cs'8 e'8 cs'8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key d \major
      \time 4/4
      
      r1 | r1 | r1 | r1 | \break
      
      fs''2 b'8 cs''8 d''8 e''8 | fs''4. d''8 fs''4. d''8 | fs''4. b'8 d''8 b'8 fs'8 d''8 | b'2    r8 e''8 d''8 cs''8 | \break
      fs''2 b'8 cs''8 d''8 e''8 | fs''4. d''8 fs''4. d''8 | fs''4. b'8 d''8 b'8 fs'8 d''8 | b'4 r4 r4      b'4        | \break
      
      cs''4 d''4 e''4 fs''8 g''8 | a''4. g''8 fs''4 g''8 a''8 | b''4. a''8 g''4 a''8 b''8 | cs'''4. b''8 fs''8 d''8 cs''8 b'8   | \break
      cs''4 d''4 e''4 fs''8 g''8 | a''4. g''8 fs''4 g''8 a''8 | b''4. a''8 g''4 a''8 b''8 | c'''4. g''8  e''4       g''8  c'''8 | \break
    }
    \new Staff {
      \clef bass
      \key d \major
      \time 4/4
      
      r1 | r1 | \"B1m35" \"B1m35" | \"B1m35" \"B1m35" |
      
      \"B1m35" \"E51m3" | \"B1m35" \"B1m35" | \"B1m35" g8 b8 fs8 as8 | \"B1m35" \"E51m3" |
      \"B1m35" \"E51m3" | \"B1m35" \"B1m35" | \"B1m35" g8 b8 fs8 as8 | \"B1m35" g4 r4    |
      
      \"A135" \"Em361" | \"Fs1m35" \"Fs1m35" | \"E1m35" \"E1m35" | \"Cs135" \"Fs135" |
      \"A135" \"Em361" | \"Fs1m35" \"Fs1m35" | \"E1m35" \"E1m35" | \"C135"  \"C135"  |
    }
    \chords {
      r1 | r1 | b2:m b2:m | b2:m b2:m |
      
      b2:m e2:m | b2:m b2:m | b2:m r2 | b2:m e2:m |
      b2:m e2:m | b2:m b2:m | b2:m r2 | b2:m r2   |
      
      a2 e2:m6 | fs2:m fs2:m | e2:m e2:m | cs2 fs2 |
      a2 e2:m6 | fs2:m fs2:m | e2:m e2:m | c2  c2  |
    }
  >>
  \layout {}
  \midi {}
}
