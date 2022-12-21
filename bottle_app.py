from bottle import *
import markdown2
import os
import shutil
import zipfile
import random
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_CSS
from infuraipfs import *
import secrets
import glob


pdfcss = """
h1, h2, h3, h4, h5, h6 { font-family: "Times"; font-weight: normal; margin-top: 32px; margin-bottom: 12px; color: #3c3b36; padding-bottom: 4px; } h1 { font-size: 1.6em; text-transform: uppercase; font-weight: bold; text-align: center; } h2 { font-size: 1.4em; text-decoration: underline; font-weight: bold; } h3 { font-size: 1.2em; text-decoration: underline; font-weight: bold; } h4, h5, h6 { font-size: 1em; font-weight: bold; } p { margin-bottom: 12px; } p:last-child { margin-bottom: 0; } ol { list-style: outside decimal; } ul { list-style: outside disc; } li > p { margin-bottom: 12px; } li > ol, li > ul { margin-top: 12px !important; padding-left: 12px; } ol:last-child, ul:last-child { margin-bottom: 12px; }
pre { white-space: pre-wrap; margin-bottom: 24px; overflow: hidden; padding: 8px; border-radius: 0px; background-color: #ececec; border-color: #d9d9d9;}
code { font-family: "Arial", monospace; font-size: 1em; white-space: nowrap; padding: 1px; border-radius: 0px; background-color: #ececec; color: #3c3b36;}
pre code { font-size: 10px; white-space: pre-wrap; }
blockquote { border-left: 5px solid grey; font-size: 90%; margin-left: 0; margin-right: auto; width: 98%; padding: 0px 2px 2px 6px; background-color: #ececec; font-family: Times; }
.theme-dark blockquote { border-color: #4d371a; } table {width:100%; border:1px solid black; border-collapse:collapse;} td , th {border:1px solid black; border-collapse:collapse; padding-top:5px; padding-bottom:5px; width:auto;} img { border: none; display: block; margin: 0 auto; } hr { border: 0; height: 1px; background-color: #ddd; } .footnote { font-size: 0.8em; vertical-align: super; } .footnotes ol { font-weight: bold; } .footnotes ol li p { font-weight: normal; }"""


# gestion du css
@route('/static/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root='./static/')


@route('/')
def index():

    txt = """<form method="post" action="/trait" accept-charset="ISO-8859-1">
	<p><label for="prev"></label><br/>
	<textarea name="txt" id="txt" rows="" cols="" wrap="virtual" style="overflow:scroll;"></textarea></p>
	<p><input type="submit" name="prevhtml" value="prevHTML"/>
	<input type="submit" name="prevpdf" value="prevPDF"/>
	<input type="submit" name="html" value="pubHTML"/>
	<input type="submit" name="pdf" value="pubPDF"/></p>
	</form>"""

    return template('index.html', txt=txt)


@post('/trait')
def traitement():

    txt = request.forms.get("txt")  # str chargée depuis formulaire textarea

    txt = txt.replace("\x92", "'")

    html = markdown2.markdown(
        txt,
        html4tags=False,
        tab_width=4,
        safe_mode=None,
        extras=[
            'fenced-code-blocks',
            'footnotes',
            'metadata',
            'pyshell',
            'smarty-pants',
            'wiki-tables'],
        link_patterns=None,
        use_file_vars=False)

    if request.POST.prevhtml:

        return template('full.html', p=html)

    elif request.POST.html:

        html = template('fullcss.html', p=html)

        rep = addtxt(html)

        h = rep['Hash']

        url = "https://oversas.org/ipfs/{0}".format(h)

        response.status = 303
        response.set_header('Location', url)

    elif request.POST.pdf:

        # restucturation du html
        html = '<!doctype html><html><head><meta charset="utf-8"><title></title></head><body>' + \
            html + '</body></html>'

        titre = secrets.token_urlsafe(8)

        # ecriture du pdf
        with open('{0}.pdf'.format(titre), 'wb') as p:

            pisa.CreatePDF(html.encode(), p, default_css=DEFAULT_CSS + pdfcss)

        rep = addfile('{0}.pdf'.format(titre))

        h = rep['Hash']

        os.remove('{0}.pdf'.format(titre))

        url = "https://oversas.org/ipfs/{0}".format(h)

        response.status = 303
        response.set_header('Location', url)

    elif request.POST.prevpdf:

        # on supprime les anciens pdf dans static

        pdf2remove = glob.glob("./static/*.pdf")

        for x in pdf2remove:

            try:
                os.remove(x)

            except OSError as e:
                pass

        # restucturation du html
        html = '<!doctype html><html><head><meta charset="utf-8"><title></title></head><body>' + \
            html + '</body></html>'

        titre = secrets.token_urlsafe(8)

        # ecriture du pdf
        with open('./static/{0}.pdf'.format(titre), 'wb') as p:

            pisa.CreatePDF(html.encode(), p, default_css=DEFAULT_CSS + pdfcss)

        response.status = 303
        response.set_header('Location', './static/{0}.pdf'.format(titre))


run(host='0.0.0.0', port=27200, reload=True, debug=True)
# application = default_app()
