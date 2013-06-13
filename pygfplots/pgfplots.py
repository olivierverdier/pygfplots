"""Module to plot using Pgfplots.

This module provides a means to create and display a graph using pgfplots.
"""

import string

class Pgf(object):
	def __init__(self, xlabel='', ylabel='', options=None):
		"""Initialize and provide axis labels."""
		self.template = string.Template(self.template_string)
		self._placeholder_dict = {}
		for key in ['tikz_header', 'tikz_footer', 'tikz_options', 'axis_options', '_contents', 'footer']:
			self._placeholder_dict[key] = []
		if options is not None:
			self['axis_options'] = options
		self.extend('axis_options', ['xlabel={{{0}}}'.format(xlabel), 'ylabel={{{0}}}'.format(ylabel)])
		self.legend = []
		self.subst_dict = {}

	template_string = r'''
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
'''

	def __getitem__(self, key):
		return self._placeholder_dict[key]

	def __setitem__(self, key, value):
		self._placeholder_dict[key] = value

	def append(self, key, value):
		self[key].append(value)

	def extend(self, key, values):
		self[key].extend(values)

	def graphics(self, name, bounding_box, options=None):
		"""
		Add an external (trimmed) graphic to the plot.
		bounding_box is in the same format as what the pyplot.axis function returns
		"""
		self['_contents'].append(r'\addplot')
		self._write_options(options)
		self['_contents'].append('graphics')
		self['_contents'].append(r'[xmin={},xmax={},ymin={},ymax={}]'.format(*bounding_box))
		self['_contents'].append(r'{%s};' % name)

	def plot(self, x, y, legend=None, options=None, force_options=False):
		r"""Plot the data contained in the vectors x and y.

		Options to the \addplot command can be provided in options.
		"""
		coor = ''.join(['({0}, {1})'. format(u, v) for u, v in zip(x, y)])
		self['_contents'].append(r'\addplot'+['+',''][force_options])
		self._write_options(options)
		self['_contents'].append('coordinates {{{}}};\n'.format(coor))
		if legend is not None:
			self.legend.append(legend)

	def render(self):
		"""
		Generate LaTeX code.
		"""
		self._add_comma('axis_options')
		self._add_comma('tikz_options')
		subst_dict = {}
		# fix legend:
		legend = ''
		if self.legend:
			## legend = r'\legend{{' + '}, {'.join(self.legend) + '}}
			legend = r'\legend{{{0}}}'.format(','.join(self.legend))
			self['_contents'].append(legend)

		for key, value in self._placeholder_dict.items():
			subst_dict[key] = '\n'.join(value)
		contents = self.template.substitute(subst_dict)
		return contents

	default_name = '.tmp_plot'

	def save(self, name=None):
		"""
		Save to a TeX file.
		If no name is given, then the file is saved to a temporary file and is then typeset.
		"""
		if isinstance(name, basestring):
			self.file_name = name
		else:
			self.file_name = self.default_name
		contents = self.render()
		with open(self.file_name + '.tex', 'w') as f:
			f.write(contents)
		if name is None: # assume that if no name is given, the pdf is to be displayed
			self.typeset(show=True)

	def typeset(self, show=False):
		"""
		Force typesetting.
		"""
		from pydflatex import Typesetter
		typesetter = Typesetter()
		typesetter.open_pdf = show
		typesetter.typeset_file(self.file_name)

	def _add_comma(self, key):
		"""
		Add trailing commas to each entry (useful for options)
		"""
		options = self[key]
		options_with_comma = [opt+', ' for opt in options]
		self[key] = options_with_comma

	def _write_options(self, options=None):
		"""
		Write options in the buffer
		"""
		if options is None:
			return
		self['_contents'].append('[')
		for option in options:
			self['_contents'].append(option+', ')
		self['_contents'].append(']')

