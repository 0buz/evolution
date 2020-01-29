import datacode.datasource as datasource

if __name__ == "__main__":
    work_file = datasource.DataFile()
    work_file.data_collect()
    work_file.remove_white_space()
    work_file.data_validate()
    preprocessed_file=work_file.data_to_csv()
    work_file.db_import(preprocessed_file)
    print(f"\n{preprocessed_file} done.")



    # test = DataFile()
    # test.data_collect()
    # test.remove_white_space()
    # test.data_validate()
    # test.data_to_csv()