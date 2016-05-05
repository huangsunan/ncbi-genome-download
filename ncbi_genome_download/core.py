import csv
import logging
import requests
from StringIO import StringIO

NCBI_URI = 'http://ftp.ncbi.nih.gov/genomes'
supported_domains = ['archaea', 'bacteria', 'fungi', 'invertebrate', 'plant',
                     'protozoa', 'unknown', 'vertebrate_mammalian',
                     'vertebrate_other', 'viral']


def download(args):
    '''Download data from NCBI'''
    if args.domain == 'all':
        for domain in supported_domains:
            _download(args.section, domain, args.uri)
    else:
        _download(args.section, args.domain, args.uri)


def _download(section, domain, uri):
    '''Download a specified domain form a section'''
    summary = get_summary(section, domain, uri)
    entries = parse_summary(summary)


def get_summary(section, domain, uri):
    '''Get the assembly_summary.txt file from NCBI and return a StringIO object for it'''
    logging.debug('Downloading summary for %r/%r uri: %r', section, domain, uri)
    url = '{uri}/{section}/{domain}/assembly_summary.txt'.format(
        section=section, domain=domain, uri=uri)
    r = requests.get(url)
    return StringIO(r.text)


def parse_summary(summary):
    '''Parse the summary file from TSV format to a csv DictReader'''
    comment = summary.read(2)
    if comment != '# ':
        idx = summary.tell()
        summary.seek(max(0, idx - 2))
    reader = csv.DictReader(summary, dialect='excel-tab')
    return reader
