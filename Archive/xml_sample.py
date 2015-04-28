from argparse import ArgumentParser
import os
import csv
import xml.sax
from pprint import pprint
from contextlib import contextmanager
from collections import OrderedDict

@contextmanager
def report_handler(outfile):
    '''Manages safe closing of the report table handler SAX parser'''
    handler = None
    try:
        handler = ReportTableContentHandler(outfile)
        yield handler
    finally:
        if handler:
            handler.close()


def clean(s):
    '''Return a copy of C{s} with spaces, backslashes, and forward slashes
    replaced with underscores.'''
    return s.replace(' ', '_').replace('\\', '_').replace('/', '_')


def open_new_output(header, outdir, file_name):
    '''Opens a new CSV output file.

    @param header: The header to write to the CSV file.
    @type header: C{list}
    @param outdir: The output directory to write the file to.
    Will be combined with C{name} to produce the final output file.
    @type outdir: C{str}
    @param file_name: The name of the output file to open.
    @type file_name: C{str}
    @return: A pair of (open file handle, csv_writer).  The file handle
    is returned so that the caller can close the handle when necessary,
    and the csv writer is returned for convenience and to avoid having to
    open a file in append mode.
    '''
    outpath = os.path.join(outdir, clean(file_name))
    outfile = open(outpath, 'wb')
    csv_writer = csv.writer(outfile, delimiter='\t')
    csv_writer.writerow(header)
    return outfile, csv_writer


class ReportTableContentHandler(xml.sax.ContentHandler):
    def __init__(self, outdir):
        xml.sax.ContentHandler.__init__(self)
        self.outdir = outdir
        self.outfile = None
        self.in_content = False
        self.counter = 0
        self.file_row_count = 1
        self.file_count = 0
        self.elements = []
        self.model_data_points = OrderedDict()
        self.caption = ''
        self.row_name = ''
        self.stats = {}
        self.stat_keys = ['Field', 'Percent', 'Mean', 'StdDev', 'Avg', 'MAD']
        self.data_keys = ['AdjustedValue', 'RawValue', 'ProfileID', 'Formula', 'VariablesMap']
        self.header = ['Caption', 'Name']
        self.header.extend(self.stat_keys)
        self.header.extend(self.data_keys)

    def elem_str(self):
        return '/'.join(self.elements)

    def close(self):
        if self.outfile:
            self.outfile.close()

    def open_new_output(self):
        self.file_row_count = 1
        self.outfile, self.csv_writer = open_new_output(self.header,
                                                        self.outdir,
                                                        '%s_%s.tsv' % (self.caption, self.file_count))

    def startElement(self, name, attrs):
        self.elements.append(name)
        #print self.elem_str()

        elem_str = self.elem_str()

        if elem_str == 'Reports/TableReport/Row':
            self.row_name = attrs.get('Name')

        if elem_str == 'Reports/TableReport/Row/Stats':
            # pull out the attributes we want and dump them in a dictionary
            self.stats = dict([(k, attrs.get(k)) for k in self.stat_keys])

        if elem_str == 'Reports/TableReport/Row/Stats/Data/DataPoint':
            # pull out the attributes we want and dump them in a dictionary
            data_point = dict([(k, attrs.get(k)) for k in self.data_keys])
            variables_map = data_point.pop('VariablesMap')
            data_row = [self.caption, self.row_name]
            data_row.extend([self.stats[k] for k in self.stat_keys])
            data_row.extend(data_point[k] for k in self.data_keys[:-1])

            if variables_map:
                data_row.extend(variables_map.split(' '))

            self.csv_writer.writerow(data_row)
            self.counter += 1
            self.file_row_count += 1

            if self.counter % 1000 == 0:
                #pass
                print '%s rows processed' % self.counter

            if self.file_row_count > 1048575:
                # stupid Excel limitations
                self.file_count += 1
                self.open_new_output()

    def endElement(self, name):
        elem_str = self.elem_str()

        # all model data points have been read for this sub-report
        if elem_str == 'Reports/TableReport':
            fname = '%s_model.csv' % clean(self.caption)

            outpath = os.path.join(self.outdir, fname)
            with open(outpath, 'wb') as ofh:
                writer = csv.writer(ofh)

                # rotate data and write out as column-oriented
                maxlen = max([len(v) for v in self.model_data_points.values()])
                row_names = self.model_data_points.keys()
                writer.writerow(row_names)
                for idx in xrange(maxlen):
                    data_row = []
                    for row_name in row_names:
                        column = self.model_data_points[row_name]
                        data_row.append(column[idx] if idx < len(column) else '')

                    writer.writerow(data_row)

        if elem_str == 'Reports/TableReport/Row/Stats/Model/Data/DataPoint':
            self.in_content = False

        # unwind part of the stack so the other event handlers know where they are
        if self.elements and self.elements[-1] == name:
            self.elements.pop()

    def characters(self, content):
        elem_str = self.elem_str()
        if elem_str == 'Reports/TableReport/Caption':
            self.caption = content
            self.file_count = 0
            self.close()

            self.open_new_output()

        if elem_str == 'Reports/TableReport/Row/Stats/Model/Data/DataPoint':
            if self.row_name not in self.model_data_points:
                self.model_data_points[self.row_name] = []

            # parser seems to call characters() more than once for a given tag
            if self.in_content:
                prev = self.model_data_points[self.row_name][-1]
                self.model_data_points[self.row_name][-1] = prev + content
            else:
                self.model_data_points[self.row_name].append(content)
                self.in_content = True

"""
if __name__ == '__main__':
    p = ArgumentParser('''Extract smoothed data model points and calculated data points from an
analysis tool XML TableDefinition.  These two sets of items together are what make up the summary
information in the report that is shown on the website.

You will need to copy the report from wherever it was originally run from, e.g.
\\psbuilder04b\c$\payscale\IndexSearch\Reports\Results\Chris PayScale Index Industry Transpo_Warehousing Delta_0.xml
''')
    p.add_argument('infile', help='Analysis tool TableDefinition input XML file')
    p.add_argument('outdir', help='Directory to place output CSV/TSV files in')

    args = p.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    with report_handler(args.outdir) as handler:
        with open(args.infile, 'rb') as ifh:
            xml.sax.parse(ifh, handler)
"""

out_dir = "C:\\users\\ryanm\\desktop\\test\\"
infile = '\\\\psstats03\\reports\\Results\\Ryan Data Dashboard Job Rollup Counts 2_0.xml'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with report_handler(out_dir) as handler:
    with open(infile, 'rb') as ifh:
        xml.sax.parse(ifh, handler)
