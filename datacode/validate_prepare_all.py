import datacode.datasource as datasource
import os


if __name__ == "__main__":
    raw_files = datasource.get_raw_files()
    print(f"{len(raw_files)} files will be processed.")
    for raw_file in raw_files:
        work_file = datasource.DataFile(raw_file)
        work_file.remove_white_space()
        work_file.data_validate()
        work_file.data_to_csv()
        print(f"\n{work_file.file} done.")

