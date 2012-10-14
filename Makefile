# TODO generate final testing report

test-unittest:
	@ echo '***************************'
	@ echo '*       Unittests         *'
	@ echo '***************************'
	@ coverage -e
	@ coverage -x tests/test_utils.py
	@ coverage -x tests/test_pywsinfo.py
	@ coverage -x tests/test_sitemap_parser.py
	@ coverage -rm pywsinfo.py

test-doctest:
	@ echo '***************************'
	@ echo '*       Doctests          *'
	@ echo '***************************'
	python -m doctest tests/test_pywsinfo.md

test-all:
	make test-unittest
	make test-doctest

todo:
	@ echo 
	@ echo "*** TODOs for pywsinfo.py ***"
	@ echo 
	@ awk '/# TODO/ { gsub(/^ /, ""); print }' pywsinfo.py
	@ echo 

graph:
	@ dot -T png docs/pywsinfo.gv -o docs/pywsinfo.png && eog docs/pywsinfo.png

test-server-start:
	@ python tests/test_server.py start

test-server-restart:
	@ python tests/test_server.py restart

test-server-stop:
	@ python tests/test_server.py stop

test-env:
	mkdir tests/log
	mkdir tests/run
	mkdir tests/static
	
test-server-env-upgrade:
	@ wget "https://raw.github.com/defnull/bottle/master/bottle.py" --no-check-certificate -O tests/packages/bottle.py	
	@ wget "https://raw.github.com/ownport/pyservice/master/pyservice.py" --no-check-certificate -O tests/packages/pyservice.py	
