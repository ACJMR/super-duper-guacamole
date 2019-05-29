test: gallery.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py gallery.mdl

gallery: simple_anim.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py simple_anim.mdl

clean:
	rm *pyc *out parsetab.py anim/*

clear:
	rm *pyc *out parsetab.py *ppm
