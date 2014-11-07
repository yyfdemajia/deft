#!/usr/bin/python2

import glob, re, string, sys

texfs = glob.glob('*.tex')
if len(sys.argv) > 1:
    texfs = sys.argv[1:]

documentclassre = re.compile(r'\\documentclass(\[[^\]]+\])?{')
graphicre = re.compile(r'^\s*\\includegraphics(\[[^\]]+\])?{([^}]+)}', re.MULTILINE)
inputre = re.compile(r'\\input(\[[^\]]+\])?{([^}]+)}')

for fname in texfs:
    f = open(fname, 'r')
    latex = f.read()
    if documentclassre.search(latex):
        pdfs = [x[1]+'.pdf' for x in graphicre.findall(latex)]
        texs = [x[1]+'.tex' for x in inputre.findall(latex)]
        if len(pdfs + texs) > 0:
            print ': %s | %s |> !latex |>' % (fname, string.join(pdfs + texs))
        else:
            print ': %s |> !latex |>' % (fname)
    else:
        print 'no good', fname