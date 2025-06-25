\version "2.24.3"

#(define title      "いつも何度でも")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 11774")
#(define total-page 2)

\include "../base.ly"

\page {
  ragged-last = ##t
}

\markup \vspace #1.5

CI = { c4  g4  c'4 }
DI = { d4  a4  d'4 }
EI = { e,4 b,4 e4  }
FI = { f,4 c4  f4  }
GI = { g,4 d4  g4  }
AI = { a,4 e4  a4  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      r4 c''4^1 e''4 | r4 c''4 e''4 | r4 c''4 e''4 | \break
      
      c''2 \A c''8 d''8 | e''8 c''8 g''4.    e''8 | d''4  g''4   d''4      | c''8^3 a'8 e''4.          c''8 | \break
      b'2     b'4       | a'4       b'4 c''8 d''8 | g'4^1 c''4^2 d''8 e''8 | f''4       f''8 e''8 d''8 c''8 | \break
      
      d''2  c''8^1 d''8 | e''8 c''8 g''4.    e''8 | d''4  g''4   d''4      | c''8^3 a'8 a'4       b'8  c''8 | \break
      g'2^1 g'4         | a'4       b'4 c''8 d''8 | g'4^1 c''4^2 d''8 e''8 | f''4       f''8 e''8 d''8 c''8 | c''2. | \break
      
      \pageBreak
      
      c''2^1 \B      e''8^2 f''8 | g''4   g''4 g''4     | g''4 g''8 a''8 g''8 f''8 | e''4   e''4      e''4       | \break
      e''4 e''8 f''8 e''8   d''8 | c''4^3 c''4 c''8 b'8 | a'4  b'4       b'8  c''8 | d''4^1 d''8 e''8 d''8  e''8 | \break
      
      d''2                e''8   f''8 | g''4 g''4    g''4      | g''4  g''8 a''8 g''8 f''8 | e''4 e''4 e''4        | \break
      e''8 f''8 e''8 d''8 c''8^3 b'8  | a'4  a'8 b'8 c''8 d''8 | g'4^1 c''4^2    d''8 e''8 | d''4.d''8 d''8[ c''8] | \break
      
      c''2.~ | c''2. | \bar "|."
      
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \CI | \CI | \CI |
      
      r2. | \CI | \GI | \AI |
      \EI | \FI | \CI | \DI |

      \GI | \CI | \GI | \AI |
      \EI | \FI | \CI | \DI | \CI |
      
      \CI | \CI | \GI | \AI |
      \EI | \AI | \FI | \GI |

      \DI | \CI | \GI | \AI |
      \EI | \FI | \CI | \GI |

      \CI | <c g c'>2. |
    }
    \chords {
      c2. | c2. | c2. |
      
      r2. | c2. | g2. | a2. |
      e2. | f2. | c2. | d2. |

      g2. | c2. | g2. | a2. |
      e2. | f2. | c2. | d2. | c2. |
      
      c2. | c2. | g2. | a2. |
      e2. | a2. | f2. | g2. |

      d2. | c2. | g2. | a2. |
      e2. | f2. | c2. | g2. |

      c2. | c2. |
    }
  >>
  \layout {}
}

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      r4 c''4^1 e''4 | r4 c''4 e''4 | r4 c''4 e''4 | \break
      
      c''2 \A c''8 d''8 | e''8 c''8 g''4.    e''8 | d''4  g''4   d''4      | c''8^3 a'8 e''4.          c''8 | \break
      b'2     b'4       | a'4       b'4 c''8 d''8 | g'4^1 c''4^2 d''8 e''8 | f''4       f''8 e''8 d''8 c''8 | \break
      
      d''2  c''8^1 d''8 | e''8 c''8 g''4.    e''8 | d''4  g''4   d''4      | c''8^3 a'8 a'4       b'8  c''8 | \break
      g'2^1 g'4         | a'4       b'4 c''8 d''8 | g'4^1 c''4^2 d''8 e''8 | f''4       f''8 e''8 d''8 c''8 | c''2. | \break
      
      \pageBreak
      
      c''2^1 \B      e''8^2 f''8 | g''4   g''4 g''4     | g''4 g''8 a''8 g''8 f''8 | e''4   e''4      e''4       | \break
      e''4 e''8 f''8 e''8   d''8 | c''4^3 c''4 c''8 b'8 | a'4  b'4       b'8  c''8 | d''4^1 d''8 e''8 d''8  e''8 | \break
      
      d''2                e''8   f''8 | g''4 g''4    g''4      | g''4  g''8 a''8 g''8 f''8 | e''4 e''4 e''4        | \break
      e''8 f''8 e''8 d''8 c''8^3 b'8  | a'4  a'8 b'8 c''8 d''8 | g'4^1 c''4^2    d''8 e''8 | d''4.d''8 d''8[ c''8] | \break
      
      c''2.~ | c''2. | \bar "|."
      
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      \CI | \CI | \CI |
      
      r2. | \CI | \GI | \AI |
      \EI | \FI | \CI | \DI |

      \GI | \CI | \GI | \AI |
      \EI | \FI | \CI | \DI | \CI |
      
      \CI | \CI | \GI | \AI |
      \EI | \AI | \FI | \GI |

      \DI | \CI | \GI | \AI |
      \EI | \FI | \CI | \GI |

      \CI | <c g c'>2. |
    }
  >>
  \midi {}
}
