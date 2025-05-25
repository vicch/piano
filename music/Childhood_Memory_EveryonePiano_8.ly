\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Childhood Memory"
  tagline = "EveryonePiano 8"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

EfiveI = { e,8 b,8 e8 r8 }
FfiveI = { f,8 c8  f8 r8 }
GfiveI = { g,8 d8  g8 r8 }
AfiveI = { a,8 e8  a8 r8 }

CI  = { c8  g8 c'8 d'8 e'8 r4. }
DmI = { d8  a8 d'8 e'8 f'8 r4. }
AmI = { a,8 e8 a8  b8  c'8 r4. }

DmII = { d,8 a,8 d8 f8 a8  d'8 r4 }
FI   = { f,8 c8  f8 a8 c'8 f'8 r4 }
GI   = { g,8 d8  g8 b8 d'8 b8  r4 }

DmIII = { d,8 a,8 d8 f8 }
FII   = { f,8 c8  f8 a8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      r2   r8 \A e'8^1  a'8^2 b'8^1 | c''4 d''8 e''8 d''4 b'8^2  g'8^1 | a'2^2         r8 e'8^1 a'8^2 b'8^1 | c''4       d''8 e''8 d''4 b'8^2 g'8^1 | \break
      e''2 r8    e''8^1 f''8  g''8  | a''4 g''8 f''8 e''4 d''4^3       | e''4 c''8 b'8 a'4^3    a'8   b'8   | c''8 e'8^1 c''8 e'8  b'4  g'4         | \break
      
      a'2  r8 \B e'8^1 a'8^2  b'8  | c''4^1 d''8 e''8 d''4      d''8 g''8   | e''2          r8 e'8^1 a'8^2 b'8 | c''4^1     d''8 e''8 d''4 d''8 g''8 | \break
      e''2.            f''8^2 g''8 | a''2             g''8 f''8 e''8 d''8^3 | e''4 c''8 b'8 a'4^3    a'8   b'8 | c''8 e'8^1 c''8 e'8  b'4  g'4       | \break

      a'2  r8 \A e'8  a'8  b'8  | c''4 d''8 e''8 d''4 b'8   g'8 | a'2           r8 e'8 a'8 b'8 | c''4     d''8 e''8 d''4 b'8 g'8 | \break
      e''2 r8    e''8 f''8 g''8 | a''4 g''8 f''8 e''4 d''4      | e''4 c''8 b'8 a'4    a'8 b'8 | c''8 e'8 c''8 e'8  b'4  g'4     | \break

      a'2.    \C      c''8^2 d''8 | e''4.  g'8^1 e''4 d''8 c''8 | d''2.      d''8^2 e''8   | f''4. a'8^1 f''4 g''4 | \break
      e''2 r8    e''8 d''8   c''8 | a''2^3       a''4 b''4      | c'''2 g''4 f''8   e''8^3 | f''4. a'8^1 f''4 g''4 | \break

      d''2.   \D      c''8   d''8 | e''4.  g'8   e''4        d''8  c''8  | d''2.                      d''8        e''8        | f''4.       a'8         f''4        g''4      | \break
      e''2 r8    e''8 d''8   c''8 | a''2         <c'' c'''>4 <d'' d'''>4 | <e'' e'''>2 r8 <g'' g'''>8 <f'' f'''>8 <e'' e'''>8 | <f'' f'''>4 <e'' e'''>4 <d'' d'''>4 <a' a''>4 | \break
      
      <e'' g'' b'' e'''>2 r8 e'8 a'8 b'8 |
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      r1   | \AfiveI \GfiveI | \AmI            | \AfiveI \GfiveI |
      \CI  | \FfiveI \GfiveI | \AfiveI \FfiveI | \AfiveI \EfiveI |
      
      \AmI | \AfiveI \GfiveI | \CI             | \AfiveI \GfiveI |
      \CI  | \FfiveI \GfiveI | \AfiveI \FfiveI | \AfiveI \EfiveI |

      \AmI | \AfiveI \GfiveI | \AmI            | \AfiveI \GfiveI |
      \CI  | \FfiveI \GfiveI | \AfiveI \FfiveI | \AfiveI \EfiveI |
      
      \AmI | \CI                       | \GI             | \DmI      |
      \CI  | \FII <a c' f'>4 <g b e'>4 | \AfiveI \GfiveI | \DmIII r2 |
      
      \GI  | \CI | \GI | \DmII |
      \CI  | \FI | \CI | \DmII |
      
      e8 b8 d'8 e'8 r2 |
    }
    \chords {
      
      r1   | a2 g2 | a1:m  | a2 g2 |
      c1   | f2 g2 | a2 f2 | a2 e2 |
      
      a1:m | a2 g2 | c1    | a2 g2 |
      c1   | f2 g2 | a2 f2 | a2 e2 |
      
      a1:m | a2 g2 | a1:m  | a2 g2 |
      c1   | f2 g2 | a2 f2 | a2 e2 |
      
      a1:m | c1       | g1    | d1:m    |
      c1   | f2 f4 g4 | a2 g2 | d2:m r2 |
      
      g1 |
    }
  >>
  \layout {}
  \midi {}
}
