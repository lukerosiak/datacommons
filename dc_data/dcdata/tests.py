
from os import remove
from unittest import TestCase
from django.db import connection

from updates import edits, update
from dcdata.contribution.sources.crp import FILE_TYPES
from dcdata.loading import model_fields
from scripts.crp.denormalize_indiv import CRPIndividualDenormalizer


class TestCRPIndividualDenormalization(TestCase):
    def test_process_record(self):
        denormalizer = CRPIndividualDenormalizer({}, {}, {})
        
        input_values = ["2000","0011161","f0000263005 ","VAN SYCKLE, LORRAINE E","C00040998","","","T2300","02/22/1999","200","","BANGOR","ME","04401","PB","15 ","C00040998","","F","VAN SYCKLE LM","99034391444","","","P/PAC"]
        input_record = dict(zip(FILE_TYPES['indivs'], input_values))
        
        output_record = denormalizer.process_record(input_record)

        self.assertEqual(set(model_fields('contribution.Contribution')), set(output_record.keys()))
        
    def test_process(self):
        denormalizer = CRPIndividualDenormalizer({}, {}, {})
        
        input_rows = [["2000","0011161","f0000263005 ","VAN SYCKLE, LORRAINE E","C00040998","","","T2300","02/22/1999","200","","BANGOR","ME","04401","PB","15 ","C00040998","","F","VAN SYCKLE LM","99034391444","","","P/PAC"],
                      ["2000","0011162","f0000180392 ","MEADOR, F B JR","C00040998","","","T2300","02/16/1999","200","","PRNC FREDERCK","MD","20678","PB","15 ","C00040998","","M","BAYSIDE CHEVROLET BUICK","99034391444","","","P/PAC"],
                      ["2000","0011163","f0000180361 ","PATKIN, MURRAY","C00040998","","","T2300","02/22/1999","500","","WATERTOWN","MA","02472","PB","15 ","C00040998","","M","TOYOTA OF WATERTOWN","99034391444","","","P/PAC"],
                      ["2000","0011164","f0000082393 ","DELUCA, WILLIAM P III","C00040998","","","T2300","02/24/1999","1000","","BRADFORD","MA","01835","PB","15 ","C00040998","","M","BILL DELUCA CHEVY PONTIAC","99034391445","","","P/PAC"],
                      ["2000","0011165","f0000180362 ","BERGER, MATTHEW S","C00040998","","","T2300","02/12/1999","2000","","GRAND RAPIDS","MI","49512","PB","15 ","C00040998","","M","BERGER CHEVROLET INC","99034391445","","","P/PAC"]]
        input_records = [dict(zip(FILE_TYPES['indivs'], row)) for row in input_rows]
        output_records = list()
        
        denormalizer.process(input_records, output_records.append)
        
        self.assertEqual(5, len(output_records))
        
    def test_execute(self):
        remove('dc_data/test_data/denormalized/denorm_indivs.08.csv')
        
        CRPIndividualDenormalizer.execute(['-c', '08', '-d', 'dc_data/test_data'])
        
        self.assertEqual(10, sum(1 for _ in open('dc_data/test_data/raw/crp/indivs08.csv', 'r')))
        self.assertEqual(11, sum(1 for _ in open('dc_data/test_data/denormalized/denorm_indivs.08.csv', 'r')))

        

# tests the experimental 'updates' module
class TestUpdates(TestCase):
    def create_table(self, table_name):
        self.cursor.execute("""create table %s ( \
                    id int not null, \
                    name varchar(255), \
                    age int, \
                    primary key (id))
                      """ % table_name)
        
    def drop_table(self, table_name):
        self.cursor.execute("drop table %s" % table_name)
        
    def insert_record(self, table_name, id, name, age):
        self.cursor.execute("insert into %s (id, name, age) values ('%s', '%s', '%s')" % (table_name, id, name, age))
        
    
    def setUp(self):
        self.cursor = connection.cursor()
        
        self.create_table('old_table')
        self.create_table('new_table')
        
    def tearDown(self):
        self.drop_table('old_table')
        self.drop_table('new_table')
        
    
    def test_edits_empty(self):
        (inserts, updates, deletes) = edits('old_table', 'new_table', 'id', ('name', 'age'))

        self.assertEqual(set([]), set(inserts))
        self.assertEqual(set([]), set(updates))
        self.assertEqual(set([]), set(deletes))
        
        update('old_table', 'new_table', 'id', ('name', 'age'))
        self.assertTablesEqual()
        

    def test_edits_empty_new(self):
        self.insert_record('old_table', 1, 'Jeremy', 29)
        self.insert_record('old_table', 2, 'Ethan', 28)
        self.insert_record('old_table', 3, 'Clay', 35)
        
        (inserts, updates, deletes) = edits('old_table', 'new_table', 'id', ('name', 'age'))

        self.assertEqual(set([]), set(inserts))
        self.assertEqual(set([]), set(updates))
        self.assertEqual(set([(1,),(2,),(3,)]), set(deletes))
        
        update('old_table', 'new_table', 'id', ('name', 'age'))
        self.assertTablesEqual()

    def test_edits_empty_old(self):
        self.insert_record('new_table', 1, 'Jeremy', 29)
        self.insert_record('new_table', 2, 'Ethan', 28)
        self.insert_record('new_table', 3, 'Clay', 35)
        
        (inserts, updates, deletes) = edits('old_table', 'new_table', 'id', ('name', 'age'))

        self.assertEqual(set([(1L, u'Jeremy', 29L), (2L, u'Ethan', 28L), (3L, u'Clay', 35L)]), set(inserts))
        self.assertEqual(set([]), set(updates))
        self.assertEqual(set([]), set(deletes))     
        
        update('old_table', 'new_table', 'id', ('name', 'age'))
        self.assertTablesEqual()   
        
        
    def test_edits(self):
        self.insert_record('old_table', 1, 'Jeremy', 29)
        self.insert_record('old_table', 2, 'Ethan', 28)
        self.insert_record('old_table', 3, 'Clay', 35)
        
        self.insert_record('new_table', 2, 'Ethan', 29)
        self.insert_record('new_table', 3, 'Clay', 35)
        self.insert_record('new_table', 4, 'Garrett', 35)

        (inserts, updates, deletes) = edits('old_table', 'new_table', 'id', ('name', 'age'))
        
        self.assertEqual(set([(4L, u'Garrett', 35L)]), set(inserts))
        self.assertEqual(set([(1,)]), set(deletes))
        self.assertEqual(set([(2L, u'Ethan', 29L)]), set(updates))
        
        update('old_table', 'new_table', 'id', ('name', 'age'))
        self.assertTablesEqual()


    def assertTablesEqual(self):
        new_table_cursor = connection.cursor()
        updated_table_cursor = connection.cursor()
        
        new_table_cursor.execute("select * from new_table order by id")        
        updated_table_cursor.execute("select * from old_table order by id")
        
        for (new_row, updated_row) in map(None, new_table_cursor, updated_table_cursor):
            self.assertEqual(new_row, updated_row)
            