from evolution import datasource as ds
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')
print(os.getcwd())


if __name__=="__main__":
    rawfile = ds.File('jira20191023.txt')
    rawfile.data_collect()
    rawfile.data_preprocess()



#
#
# rawfile = File('raw20191023.txt')
# xxx=rawfile.output()
# rawfile.data_collect()
# rawfile.data_preprocess()
# with open(str(xxx), "a") as f:
#     f.write("\naaaaaa")
# logging.getLogger("info_logger").info("test jobs extracted.")
#
# curr_date = filter(lambda x: x != "-", str(date.today()))
# basename = f"raw{''.join(curr_date)}xxx.txt"
# outputname = re.sub('^raw(.*)txt$', 'preprocessed\\1csv', basename)