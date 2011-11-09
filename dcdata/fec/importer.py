import urllib
import os
import subprocess
import re
from collections import namedtuple
import tempfile

from django.db import connection


F = namedtuple('F', ['url', 'dta_file', 'schema_file', 'sql_table'])

FEC_CONFIG = [
    F('ftp://ftp.fec.gov/FEC/cm12.zip', 'foiacm.dta', 'fec_committee_master_schema.csv', 'fec_committees'),
    F('ftp://ftp.fec.gov/FEC/cn12.zip', 'foiacn.dta', 'fec_candidate_master_schema.csv', 'fec_candidates'),
    F('ftp://ftp.fec.gov/FEC/indiv12.zip', 'itcont.dta', 'fec_individual_contributions.csv', 'fec_indiv_import'),
    F('ftp://ftp.fec.gov/FEC/pas212.zip', 'itoth.dta', 'fec_contributions_to_candidates.csv', 'fec_pac2cand'),
    F('ftp://ftp.fec.gov/FEC/oth12.zip', 'itpas2.dta', 'fec_committee_transactions.csv', 'fec_pac2pac')
]

SCHEMA_ROOT = os.path.abspath('../ffs/us/fec/')


def download(destination_dir):
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)
    
    for conf in FEC_CONFIG:
        local_file = os.path.join(destination_dir, conf.url.split("/")[-1])
        urllib.urlretrieve(conf.url, local_file)
        

def extract(source_dir):
    abs_source = os.path.expanduser(source_dir)
    subprocess.check_call(['unzip', os.path.join(abs_source, "*.zip"), "-d" + abs_source])
    
    
def fix_unicode(source_dir):
    abs_source = os.path.expanduser(source_dir)
    for conf in FEC_CONFIG:
        infile = open(os.path.join(abs_source, conf.dta_file), 'r')
        outfile = open(os.path.join(abs_source, conf.dta_file + ".utf8"), 'w')
        
        for line in infile:
            fixed_line = line.decode('utf8', 'replace').encode('utf8', 'replace')
            outfile.write(fixed_line)


def fec_2_csv(source_dir):
    abs_source = os.path.expanduser(source_dir)
    for conf in FEC_CONFIG:       
        outfile = open(os.path.join(abs_source, conf.dta_file.split(".")[0] + ".csv"), 'w')
        subprocess.check_call(
            ['in2csv', '--f=fixed', '--schema=%s' % os.path.join(SCHEMA_ROOT, conf.schema_file), os.path.join(abs_source, conf.dta_file + ".utf8")],
            stdout=outfile)


def upload(source_dir):
    abs_source = os.path.expanduser(source_dir)
    c = connection.cursor()
    
    for conf in FEC_CONFIG:
        infile = open(os.path.join(abs_source, conf.dta_file.split(".")[0] + ".csv"), 'r')
        c.execute("DELETE FROM %s" % conf.sql_table)
        c.copy_expert("COPY %s FROM STDIN CSV HEADER" % conf.sql_table, infile)


def reload_fec(dir=None):
    if not dir:
        dir = tempfile.mkdtemp()
    
    print "Downloading files to %s..." % dir
    download(dir)
    
    print "Extracting files..."
    extract(dir)
    
    print "Converting to unicode..."
    fix_unicode(dir)
    
    print "Concerting to CSV..."
    fec_2_csv(dir)
    
    print "Uploading data..."
    upload(dir)
    
    print "Done."
    