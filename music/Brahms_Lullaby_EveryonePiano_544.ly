\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Brahms' Lullaby"
  tagline = "EveryonePiano 544"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

C        = { c8[ g8]  c'8[ g8]  c'8[ g8]  }
Cseveni  = { c8[ g8]  bf8[ g8]  bf8[ g8]  }
Csevenii = { g8[ bf8] c'8[ bf8] c'8[ bf8] }
Fi       = { f8[ a8]  c'8[ a8]  c'8[ a8]  }
Fii      = { f8[ a8]  c'8[ a8]  f4        }
As       = { f8[ bf8] d'8[ bf8] d'8[ bf8] }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 3/4
      
      \partial 4 a'8^1 a'8 | c''4.^2 a'8       a'4         | c''2             a'8   c''8   | f''4^5             e''4. d''8 | d''4      c''4  g'8^1 a'8 | \break
                           | bf'4    g'4       g'8    a'8  | bf'2             g'8^1 bf'8^2 | e''8^4 d''8        c''4  e''4 | f''2            f'8^1 f'8 | \break
                           | <<d''2^3 f''2^5>> d''8^5 bf'8 | <<a'2^2 c''2^4>> a'8^2 f'8^1  | bf'4               c''4  d''4 | a'8 c''8( c''4) f'8   f'8 | \break
                           | <<d''2   f''2>>   d''8   bf'8 | <<a'2   c''2>>   a'8   f'8    | bf'8^4 c''16 bf'16 a'4   g'4  | f'2.                      | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 3/4
      
      r4 | \Fi       | \Fi       | \As      | \Fi  |
         | \Csevenii | \Csevenii | \Cseveni | \Fii |
         | \As       | \Fi       | \C       | \Fi  |
         | \As       | \Fi       | \Cseveni | \Fii |
    }
    \chords {
      r4 | f2.   | f2.   | as2.  | f2. |
         | c2.:7 | c2.:7 | c2.:7 | f2. |
         | as2.  | f2.   | c2.   | f2. |
         | as2.  | f2.   | c2.:7 | f2. |
    }
  >>
  \layout {}
  \midi {}
}
