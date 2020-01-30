import datacode.datasource as datasource
import os

if __name__ == "__main__":
    raw_files = datasource.get_files('raw')
    print(f"{len(raw_files)} files will be processed.")
    total_records = 0
    for raw_file in sorted(raw_files):
        work_file = datasource.DataFile(raw_file)
        work_file.remove_white_space()
        work_file.data_validate()
        preprocessed_file = work_file.data_to_csv()
        total_records += work_file.record_count
        work_file.db_import(preprocessed_file)
        print(f"\n{preprocessed_file} done.")

    # validation=datasource.DataFile('raw20191023.txt')
    # validation.remove_white_space()
    # validation.data_validate()
    # preprocessed_file = validation.data_to_csv()
    # #total_records+=validation.record_count
    # validation.db_import(preprocessed_file)
    # print(f"\n{preprocessed_file} done.")
