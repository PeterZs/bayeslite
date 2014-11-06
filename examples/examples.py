# -*- coding: utf-8 -*-

########################################################################
# XXX THESE ARE REALLY BAD EXAMPLES THEY SERVE ONLY TO SEE WHETHER THE #
# WHOLE CODE IS GOING TO CRASH AND BURN DON'T RELY ON THEM PLEASE XXX  #
########################################################################

import bayeslite
import crosscat.CrossCatClient

crosscat = crosscat.CrossCatClient.get_CrossCatClient("local", seed=0)

bdb = bayeslite.BayesDB(crosscat)
bdb.sqlite.execute("""
    create table zoot (
        key integer primary key,
        label text,
        age double,
        weight double
    );
""")
bdb.sqlite.executemany("insert into zoot (label,age,weight) values (?,?,?)", [
    ('foo', 12, 24),
    ('bar', 14, 28),
    (None, 10, 20),
    ('baz', None, 32),
    ('quux', 4, None),
    ('zot', 8, 16),
    ('mumble', 8, 16),
    ('frotz', 8, 16),
    ('gargle', 8, 16),
    ('mumph', 8, 16),
    ('hunf', 11, 22),
    ('blort', 16, 32),
    (None, 16, 32),
    (None, 17, 34),
    (None, 18, 36),
    (None, 19, 38),
    (None, 20, 40),
    (None, 21, 42),
    (None, 22, 44),
    (None, 23, 46),
    (None, 24, 48),
    (None, 25, 50),
    (None, 26, 52),
    (None, 27, 54),
    (None, 28, 56),
    (None, 29, 58),
    (None, 30, 60),
    (None, 31, 62),
])
bayeslite.bayesdb_import_sqlite_table(bdb, "zoot")
print "### bayesdb_table"
for x in bdb.sqlite.execute("select * from bayesdb_table"): print x
print "### bayesdb_table_column"
for x in bdb.sqlite.execute("select * from bayesdb_table_column"): print x
for x in bdb.sqlite.execute("select column_correlation(1, 2, 3)"): print x
nmodels = 4
bayeslite.bayesdb_models_initialize(bdb, 1, nmodels)
for i in range(nmodels):
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
    bayeslite.bayesdb_models_analyze1(bdb, 1, i)
print bayeslite.bayesdb_infer(bdb, 1, 2, 4, None, 0.1, numsamples=1)
print bayeslite.bayesdb_infer(bdb, 1, 3, 5, None, 0.1, numsamples=1)

for x in bayeslite.bayesdb_simulate(bdb, 1, [(2, 42)], [0, 1, 2, 3], 10):
    print x

bayeslite.bayesdb_import_csv_file(bdb, "flights", "flights.csv")

cdb = bayeslite.BayesDB(crosscat)
bayeslite.bayesdb_import_csv_file(cdb, "flights", "flights.csv")
bayeslite.bayesdb_import_csv_file(cdb, "dha", "dha.csv")
dha_id = bayeslite.sqlite3_exec_1(cdb.sqlite,
    "SELECT id FROM bayesdb_table WHERE name = 'dha'")
for x in cdb.sqlite.execute("SELECT * FROM bayesdb_table"): print x
for x in cdb.sqlite.execute("SELECT * FROM bayesdb_table_column"): print x
dha_nmodels = 10
bayeslite.bayesdb_models_initialize(cdb, dha_id, dha_nmodels)
for i in range(dha_nmodels):
    print "--- analyze model %d of table %d" % (i, dha_id)
    bayeslite.bayesdb_models_analyze1(cdb, dha_id, i)
# ESTIMATE COLUMNS FROM dha
# WHERE TYPICALITY > 0.4
# ORDER BY DEPENDENCE PROBABILITY WITH N_DEATH_ILL
estimate_columns = """
    SELECT c.name
      FROM bayesdb_table_column AS c
     WHERE c.table_id = (SELECT id FROM bayesdb_table WHERE name = 'dha')
       AND column_typicality(c.table_id, c.colno) > 0.4
     ORDER BY column_dependence_probability(c.table_id, c.colno,
                  (SELECT colno FROM bayesdb_table_column
                    WHERE table_id = c.table_id AND name = 'N_DEATH_ILL'))
"""
for x in cdb.sqlite.execute(estimate_columns): print x