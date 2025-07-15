\version "2.24.3"

#(define title      "Brahms' Lullaby")
#(define title-font "")
#(define sequence   "EveryonePiano 544")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

"C158585" = { c8[ g8] c'8[ g8] c'8[ g8] }

"C5b71b71b7" = { g8[ bf8] c'8[ bf8] c'8[ bf8] }
"C15b75b75"  = { c8[ g8]  bf8[ g8]  bf8[ g8]  }

"F135353" = { f8[ a8] c'8[ a8] c'8[ a8] }
"F13531"  = { f8[ a8] c'8[ a8] f4       }

"As513131" = { f8[ bf8] d'8[ bf8] d'8[ bf8] }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 3/4
      
      \partial 4 a'8^1 a'8 | c''4.^2 a'8 a'4     | c''2 a'8   c''8   | f''4^5      e''4. d''8 | \break
      d''4 c''4  g'8^1 a'8 | bf'4    g'4 g'8 a'8 | bf'2 g'8^1 bf'8^2 | e''8^4 d''8 c''4  e''4 | \break
      
      f''2           f'8^1 f'8 | <<d''2^3 f''2^5>> d''8^5 bf'8 | <<a'2^2 c''2^4>> a'8^2 f'8^1 | bf'4               c''4 d''4 | \break
      a'8 c''8~ c''4 f'8   f'8 | <<d''2   f''2>>   d''8   bf'8 | <<a'2   c''2>>   a'8   f'8   | bf'8^4 c''16 bf'16 a'4  g'4  | f'2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 3/4
      
      r4         | \"F135353"    | \"F135353"    | \"As513131"  |
      \"F135353" | \"C5b71b71b7" | \"C5b71b71b7" | \"C15b75b75" |
      
      \"F13531"  | \"As513131" | \"F135353" | \"C158585"   |
      \"F135353" | \"As513131" | \"F135353" | \"C15b75b75" | \"F13531" |
    }
    \chords {
      r4  | f2.   | f2.   | as2.  |
      f2. | c2.:7 | c2.:7 | c2.:7 |
      
      f2. | as2. | f2. | c2.   |
      f2. | as2. | f2. | c2.:7 | f2. |
    }
  >>
  \layout {}
  \midi {}
}
