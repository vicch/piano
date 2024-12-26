\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "いつも何度でも"
  tagline = "EveryonePiano 11774"
}

\paper {
  total-page = 2
  ragged-last = ##t
}

\markup \vspace #1.5

Cfive = { c4  g4  c'4 }
Dfive = { d4  a4  d'4 }
Efive = { e,4 b,4 e4  }
Ffive = { f,4 c4  f4  }
Gfive = { g,4 d4  g4  }
Afive = { a,4 e4  a4  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      r4 c''4 e''4 | r4 c''4 e''4 | r4 c''4 e''4 | c''2 c''8 d''8 | \break
      
      e''8 c''8 g''4~ g''8 e''8 | d''4 g''4 d''4 | c''8 a'8 e''4~ e''8 c''8 | b'2 b'4 | \break a'4 b'4 c''8 d''8 | g'4 c''4 d''8 e''8 | f''4 f''8 e''8 d''8 c''8 | d''2 c''8 d''8 | \break
      e''8 c''8 g''4~ g''8 e''8 | d''4 g''4 d''4 | c''8 a'8 a'4   b'8  c''8 | g'2 g'4 | \break a'4 b'4 c''8 d''8 | g'4 c''4 d''8 e''8 | f''4 f''8 e''8 d''8 c''8 | c''2.          | \break
      
      \pageBreak
      
      c''2 e''8 f''8 | g''4 g''4 g''4 | g''4 g''8 a''8 g''8 f''8 | e''4 e''4 e''4 | \break e''4      e''8 f''8 e''8 d''8 | c''4 c''4    c''8 b'8  | a'4 b'4  b'8  c''8 | d''4 d''8 e''8 d''8  e''8  | \break
      d''2 e''8 f''8 | g''4 g''4 g''4 | g''4 g''8 a''8 g''8 f''8 | e''4 e''4 e''4 | \break e''8 f''8 e''8 d''8 c''8 b'8  | a'4  a'8 b'8 c''8 d''8 | g'4 c''4 d''8 e''8 | d''4.     d''8 d''8[ c''8] | \break
      
      c''2.~ | c''2. | \bar "|."
      
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \Cfive | \Cfive | \Cfive | r2. |
      
      \Cfive | \Gfive | \Afive | \Efive | \Ffive | \Cfive | \Dfive | \Gfive |
      \Cfive | \Gfive | \Afive | \Efive | \Ffive | \Cfive | \Dfive | \Cfive |
      
      \Cfive | \Cfive | \Gfive | \Afive | \Efive | \Afive | \Ffive | \Gfive |
      \Dfive | \Cfive | \Gfive | \Afive | \Efive | \Ffive | \Cfive | \Gfive |
      
      \Cfive | <c g c'>2. |
    }
    \chords {
      c2.:5 | c2.:5 | c2.:5 | r2. |
      
      c2.:5 | g2.:5 | a2.:5 | e2.:5 | f2.:5 | c2.:5 | d2.:5 | g2.:5 |
      c2.:5 | g2.:5 | a2.:5 | e2.:5 | f2.:5 | c2.:5 | d2.:5 | c2.:5 |
      
      c2.:5 | c2.:5 | g2.:5 | a2.:5 | e2.:5 | a2.:5 | f2.:5 | g2.:5 |
      d2.:5 | c2.:5 | g2.:5 | a2.:5 | e2.:5 | f2.:5 | c2.:5 | g2.:5 |
      
      c2.:5 | c2.:5 |
    }
  >>
  \layout {}
  \midi {}
}
