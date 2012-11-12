#!/usr/bin/env python
import json
from messytables import (
    CSVTableSet,
    headers_guess,
    headers_processor,
    offset_processor,
    type_guess,
    DateType,
    StringType,
    IntegerType,
    FloatType,
    DecimalType)

def main():
    f = open('testdata/csv/simple.csv')
    table_set = CSVTableSet.from_fileobj(f)
    row_set = table_set.tables.pop()
    offset, headers = headers_guess(row_set.sample)

    fields = []
    dup_columns = {}
    noname_count = 1
    guess_types = [StringType, IntegerType, FloatType, DecimalType, DateType]
    row_types = type_guess(row_set.sample, guess_types)
    for index, field in enumerate(headers):
        field_dict = {}
        if "" == field:
            field = '_'.join(['column', str(noname_count)])
            headers[index] = field
            noname_count += 1
        if headers.count(field) == 1:
            field_dict['id'] = field
        else:
            dup_columns[field] = dup_columns.get(field, 0) + 1
            field_dict['id'] =  u'_'.join([field, str(dup_columns[field])])
        if isinstance(row_types[index], DateType): # is row_types[index]:
            field_dict['type'] = 'DateTime'
            field_dict['format'] = row_types[index].format
        else:
            field_dict['type'] = str(row_types[index])
        fields.append(field_dict)
    row_set.register_processor(headers_processor([x['id'] for x in fields]))
    row_set.register_processor(offset_processor(offset + 1))

    data_row = {}
    result = []
    for row in row_set:
        for index, cell in enumerate(row):
            data_row[cell.column] = cell.value
        result.append(data_row)
    result_data = {'headers': fields, 'data': result}
    result_json = json.dumps(result_data)
    print result_json


if __name__ == '__main__':
    main()