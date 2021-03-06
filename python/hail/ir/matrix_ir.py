import json
from hail.ir.base_ir import *
from hail.utils.java import escape_str, escape_id, parsable_strings

class MatrixAggregateRowsByKey(MatrixIR):
    def __init__(self, child, expr):
        super().__init__()
        self.child = child
        self.expr = expr

    def __str__(self):
        return '(MatrixAggregateRowsByKey {} {})'.format(self.child, self.expr)


class MatrixRead(MatrixIR):
    def __init__(self, path, drop_cols, drop_rows):
        super().__init__()
        self.path = path
        self.drop_cols = drop_cols
        self.drop_rows = drop_rows

    def __str__(self):
        config = dict(
            name='MatrixNativeReader',
            path=self.path
        )
        return f'(MatrixRead None {self.drop_cols} {self.drop_rows} "{escape_str(json.dumps(config))}")'


class MatrixRange(MatrixIR):
    def __init__(self, n_rows, n_cols, n_partitions):
        super().__init__()
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_partitions = n_partitions

    def __str__(self):
        config = dict(
            name='MatrixRangeReader',
            nRows=self.n_rows,
            nCols=self.n_cols,
            nPartitions=self.n_partitions
        )
        return f'(MatrixRead None False False "{escape_str(json.dumps(config))}")'

class MatrixImportVCF(MatrixIR):
    def __init__(self,
                 paths,
                 force,
                 force_bgz,
                 header_file,
                 min_partitions,
                 drop_samples,
                 call_fields,
                 reference_genome,
                 contig_recoding,
                 array_elements_required,
                 skip_invalid_loci):
        super().__init__()
        self.paths = paths
        self.force = force
        self.force_bgz = force_bgz
        self.header_file = header_file
        self.min_partitions = min_partitions
        self.drop_samples = drop_samples
        self.call_fields = call_fields
        self.reference_genome = reference_genome
        self.contig_recoding = contig_recoding
        self.array_elements_required = array_elements_required
        self.skip_invalid_loci = skip_invalid_loci

    def __str__(self):
        config = dict(
            name='MatrixVCFReader',
            files=self.paths,
            callFields=list(self.call_fields),
            headerFile=self.header_file,
            minPartitions=self.min_partitions,
            rg=self.reference_genome.name if self.reference_genome else None,
            contigRecoding=self.contig_recoding,
            arrayElementsRequired=self.array_elements_required,
            skipInvalidLoci=self.skip_invalid_loci,
            gzAsBGZ=self.force_bgz,
            forceGZ=self.force
        )
        return f'(MatrixImportVCF "{json.dumps(config)}" {self.drop_samples} False None)'

class MatrixFilterRows(MatrixIR):
    def __init__(self, child, pred):
        super().__init__()
        self.child = child
        self.pred = pred

    def __str__(self):
        return '(MatrixFilterRows {} {})'.format(self.child, self.pred)

class MatrixChooseCols(MatrixIR):
    def __init__(self, child, old_entries):
        super().__init__()
        self.child = child
        self.old_entries = old_entries

    def __str__(self):
        return '(MatrixChooseCols ({}) {})'.format(
            self.child, ' '.join([str(i) for i in self.old_entries]))

class MatrixMapCols(MatrixIR):
    def __init__(self, child, new_col, new_key):
        super().__init__()
        self.child = child
        self.new_col = new_col
        self.new_key = new_key

    def __str__(self):
        return '(MatrixMapCols {} {} {})'.format(
            '(' + ' '.join([escape_id(f) for f in self.new_col]) + ')' if self.new_col else 'None',
            self.child, self.new_col)

class MatrixMapEntries(MatrixIR):
    def __init__(self, child, new_entry):
        super().__init__()
        self.child = child
        self.new_entry = new_entry

    def __str__(self):
        return '(MatrixMapEntries {} {})'.format( self.child, self.new_entry)

class MatrixFilterEntries(MatrixIR):
    def __init__(self, child, pred):
        super().__init__()
        self.child = child
        self.pred = pred

    def __str__(self):
        return '(MatrixFilterEntries {} {})'.format(self.child, self.pred)

class MatrixMapRows(MatrixIR):
    def __init__(self, child, new_row, new_key):
        super().__init__()
        self.child = child
        self.new_row = new_row
        self.new_key = new_key

    def __str__(self):
        return '(MatrixMapEntries {} {} {})'.format(
            '(' + ' '.join([escape_id(f) for (f, _) in self.new_key]) if self.new_key else 'None',
            '(' + ' '.join([escape_id(f) for (_, f) in self.new_key]) if self.new_key else 'None',
            self.child, self.new_row)

class MatrixMapGlobals(MatrixIR):
    def __init__(self, child, new_row, value):
        super().__init__()
        self.child = child
        self.new_row = new_row
        self.value = value

    def __str__(self):
        return '(MatrixMapGlobals {} {} {})'.format(
            escape_str(json.dumps(self.value)),
            self.child, self.pred)

class MatrixFilterCols(MatrixIR):
    def __init__(self, child, pred):
        super().__init__()
        self.child = child
        self.pred = pred

    def __str__(self):
        return '(MatrixFilterCols {} {})'.format(self.child, self.pred)

class MatrixCollectColsByKey(MatrixIR):
    def __init__(self, child):
        super().__init__()
        self.child = child

    def __str__(self):
        return '(MatrixCollectColsByKey {})'.format(self.child)

class MatrixAggregateColsByKey(MatrixIR):
    def __init__(self, child, agg_ir):
        super().__init__()
        self.child = child
        self.agg_ir = agg_ir

    def __str__(self):
        return '(MatrixAggregateColsByKey {} {})'.format(self.child, self.agg_ir)

class TableToMatrixTable(MatrixIR):
    def __init__(self, child, row_key, col_key, row_fields, col_fields, partition_key, n_partitions):
        super().__init__()
        self.child = child
        self.row_key = row_key
        self.col_key = col_key
        self.row_fields = row_fields
        self.col_fields = col_fields
        self.partition_key = partition_key
        self.n_partitions = n_partitions

    def __str__(self):
        return f'(TableToMatrixTable ' \
               f'{parsable_strings(self.row_key)} ' \
               f'{parsable_strings(self.col_key)} ' \
               f'{parsable_strings(self.row_fields)} ' \
               f'{parsable_strings(self.col_fields)} ' \
               f'{parsable_strings(self.partition_key)} ' \
               f'{"None" if self.n_partitions is None else str(self.n_partitions)} ' \
               f'{self.child})'

class MatrixExplodeRows(MatrixIR):
    def __init__(self, child, path):
        super().__init__()
        self.child = child
        self.path = path

    def __str__(self):
        return '(MatrixExplodeRows ({}) {})'.format(
            ' '.join([escape_id(id) for id in self.path]),
            self.child)
