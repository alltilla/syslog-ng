EXTRA_DIST += \
	contrib/config_option_database/config_database.py \
	contrib/config_option_database/requirements.txt \
	contrib/config_option_database/__init__.py \
	contrib/config_option_database/utils/BisonGraph.py \
	contrib/config_option_database/utils/ConfigOptions.py \
	contrib/config_option_database/utils/OptionParser.py \
	contrib/config_option_database/utils/Yacc2Graph.py \
	contrib/config_option_database/utils/__init__.py \
	contrib/config_option_database/utils/test/test_BisonGraph.py \
	contrib/config_option_database/utils/test/test_OptionParser.py \
	contrib/config_option_database/utils/test/test_Yacc2Graph.py

contrib/config_option_database/.cache/options.json:
	${top_srcdir}/contrib/config_option_database/config_database.py --rebuild

bin_SCRIPTS += contrib/config_option_database/config_database.py \
	contrib/config_option_database/.cache/options.json
