\version "2.24.3"
\include "../template.v1.ly"

\paper {
  ragged-last = ##t
}

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "白桦林"
  tagline = "EveryonePiano 1056"
}

\markup \vspace #1.5

C  = { c4  <<e4  g4>>  <<e4  g4>>  }
Dm = { d4  <<f4  a4>>  <<f4  a4>>  }
E  = { e4  <<gs4 b4>>  <<gs4 b4>>  }
Em = { e,4 <<g,4 b,4>> <<g,4 b,4>> }
G  = { g,4 <<b,4 d4>>  <<b,4 d4>>  }
Am = { a,4 <<c4  e4>>  <<c4  e4>>  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      e'4.^1  f'8^2  e'4^1          | c''2^5         a'4^3        | b'4.^4         c''8^5 b'8^4  a'8^3  | e'2.^1  | d'4.^1  e'8^2  d'4^1         | b'4^5  a'4^4         d'4^1       | e'4^2     gs'4^3     b'4^5         | a'2.^4  | \break
      a'4^1   bf'4^2 a'4^1          | a''2^5         e''4^2       | f''4.^3        g''8^4 f''8^3 d''8^1 | e''2.^2 | e''4.^3 c''8^1 d''8^2 e''8^3 | d''2^2               c''4^1      | b'4^2     e'4^1      e''8^5 d''8^4 | a'2.^1  | \break
      a''4.^5 e''8^2 e''8^2  f''8^3 | f''4.^3 d''8^2 a'8^1 d''8^2 | g''4^4  g''8^4 a''8^5 g''8^4 a''8^5 | e''2.^2 | e''4.^5 d''8^4 c''8^3 b'8^2  | e'4^1  d''8^5 c''8^4 b'8^3 a'8^2 | b'8^1 b'8 b'8 e''8^3 e''8   d''8^2 | e''2.^3 | \break
      a''4.^3 b''8^4 c'''8^5 b''8^4 | f''4.^1 d''8^2 a'8^1 d''8^2 | g''4^3  a''4^4        b''4^5        | e''2.^1 | e''4.^3 c''8^1 d''8^2 e''8^3 | d''2^2               c''4^1      | b'4^2     e'4^1      e''8^5 d''8^4 | a'2.^1~ | \break
      a'2.~                         | a'2.                        | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \E  | \Am        | \E  | \E | \Dm | \Dm | \E | \Am |
      \Am | \Am        | \Dm | \E | \Am | \E  | \E | \Am |
      \Am | \Dm        | \G  | \C | \E  | \E  | \E | \E  |
      \Am | \Dm        | \G  | \C | \C  | \E  | \E | \Am |
      \Em | <a, c e>2. |
    }
    \chords {
      e   | a:m | e   | e | d:m | d:m | e | a:m |
      a:m | a:m | d:m | e | a:m | e   | e | a:m |
      a:m | d:m | g   | c | e   | e   | e | e   |
      a:m | d:m | g   | c | c   | e   | e | a:m |
      e:m | a:m |
    }
  >>
  \layout {}
  \midi {}
}
