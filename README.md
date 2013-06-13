# `pygfplots`: High quality plots with pgfplots and Python

The aim of this package is to make it easier to create nice looking graphs using data from Python programs.
Here is a (rather advanced) example of that, which serves as a documentation of this package:

```python
import numpy as np
xs = np.linspace(-1, 1, 300)
p = Pgf('$x$', '$T(x)$')
p.append('axis_options', 'cycle list name=color list')
p.append('axis_options', 'legend pos=outer north east')
p.append('axis_options', 'title={Chebyshev Polynomials}')
from numpy.polynomial.chebyshev import Chebyshev
for n in range(8):
	f = Chebyshev([0]*n+[1])
	p.plot(xs, f(xs), legend='$T_{0}$'.format(n), options=['smooth', 'thick', 'opacity=.6'])
p.append('tikz_header', r'\tikzset{>=stealth}')
p.append('footer', r'\path[draw=gray, thick] (axis cs:-1,-1) -- (axis cs:-1,1) -- (axis cs:1,1) -- (axis cs:1,-1) -- cycle;')
p.append('footer', r'\node[shape=circle, draw, fill opacity=.5, fill=white] (zero) at (axis cs:-.5,-.5) {};')
p.append('footer', r'\node[right, opacity=.8, fill=white, text opacity=1, draw=gray] (zero_label) at (axis cs:-.5,.5) {Interesting point};')
p.append('tikz_footer', '\draw[->,very thick] (zero_label) to[out=180,in=150] (zero);')
p.save() # for interactive visualisation
p.save('example') # to save to a tex file "example.tex"
```

The general structure of the template is
```tex
\documentclass{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.5.1}
$tikz_header
\begin{document}
\begin{tikzpicture}
[$tikz_options
]
\begin{axis}
[$axis_options
]
$_contents

$footer

\end{axis}
$tikz_footer
\end{tikzpicture}
\end{document}
```
