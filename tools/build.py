import pathlib
r = pathlib.Path(__file__).resolve().parent.parent
shell = (r/'src/shell.html').read_text(encoding='utf-8'); js = (r/'src/app.js').read_text(encoding='utf-8')
(r/'index.html').write_text(shell.replace('/*JS*/', js), encoding='utf-8'); print('built', len(js))
