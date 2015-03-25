# -*- coding: utf-8 -*-

#   Copyright (c) 2010-2014, MIT Probabilistic Computing Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import csv
import json
import math

import bayeslite.core as core

def bayesdb_load_codebook_csv_file(bdb, table, pathname):
    codebook = None
    with open(pathname, 'rU') as f:
        reader = csv.reader(f)
        try:
            header = reader.next()
        except StopIteration:
            raise IOError('Empty codebook file')
        header = [unicode(h, 'utf8').strip() for h in header]
        if header != ['column_label','short_name','description','value_map']:
            raise IOError('Wrong CSV header for codebook')
        codebook = []
        line = 1
        for row in reader:
            if len(row) != 4:
                raise IOError('Wrong number of columns at line %d: %d' %
                    (line, len(row)))
            column_name, _shortname, _description, _value_map_json = row
            codebook.append(row)
            line += 1
    with bdb.savepoint():
        for column_name, shortname, description, value_map_json in codebook:
            if not core.bayesdb_table_has_column(bdb, table, column_name):
                raise IOError('Column does not exist in table %s: %s' %
                    (repr(table), repr(column_name)))
            colno = core.bayesdb_table_column_number(bdb, table, column_name)
            value_map = json.loads(value_map_json)
            if isinstance(value_map, float) and math.isnan(value_map):
                # No value map.
                pass
            elif isinstance(value_map, dict):
                sql = '''
                    DELETE FROM bayesdb_column_map
                        WHERE tabname = ? AND colno = ?
                '''
                bdb.sql_execute(sql, (table, colno))
                sql = '''
                    INSERT INTO bayesdb_column_map
                        (tabname, colno, key, value)
                        VALUES (?, ?, ?, ?)
                '''
                for key in sorted(value_map.keys()):
                    value = value_map[key]
                    bdb.sql_execute(sql, (table, colno, key, value))
            else:
                # XXX Arbitrary input in error message...
                raise IOError('Invalid value map for column: %s' %
                    (repr(column_name),))
            sql = '''
                UPDATE bayesdb_column
                    SET shortname = ?, description = ?
                    WHERE tabname = ? AND colno = ?
            '''
            bdb.sql_execute(sql, (shortname, description, table, colno))
