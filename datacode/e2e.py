import datacode.datasource as datasource
import os


if __name__ == "__main__":
    work_file = datasource.DataFile()
    work_file.data_collect()
    work_file.remove_white_space()
    work_file.data_validate()
    work_file.data_to_csv()
    work_file.db_import()
    print(f"\n{work_file.file} done.")



    test = DataFile()
    test.data_collect()
    test.remove_white_space()
    test.data_validate()
    test.data_to_csv()