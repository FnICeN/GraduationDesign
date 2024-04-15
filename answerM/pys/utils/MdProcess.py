import pandas as pd
class Processor:
    def __init__(self, root_path):
        self.rootpath = root_path

    def generateMd(self, N):
        df = pd.read_csv(self.rootpath + "/GraduationDesign/语料库/客服语料/" + str(N) + ".md", sep='|')
        #删除第一列
        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[2], axis=1, inplace=True)
        #删除第一行
        df.drop(0, axis=0, inplace=True)
        # 删除空行
        df.dropna(axis=0, how='all', inplace=True)
        df = df.reset_index(drop=True)
        # 删除包含“问题”或“-”的行
        for i in range(0, len(df)):
            if ("问题" == df.loc[i][0].strip()) or ("-" in df.loc[i][0]):
                df.drop(i, axis=0, inplace=True)
        df = df.reset_index(drop=True)
        df = df.apply(lambda x: x.str.strip())
        # 去除df列名中的空格
        df.columns = df.columns.map(lambda x: x.strip())
        df.to_csv(self.rootpath + "/GraduationDesign/语料库/客服语料/整理后/" + str(N) + ".csv", index=False)
        print("处理完成，生成文件：{}.csv，此文件共{}行".format(N, len(df)))

    def concatCsv(self, ra : list):
        df = pd.read_csv(self.rootpath + "/GraduationDesign/语料库/客服语料/整理后/" + str(ra[0]) + ".csv")
        for i in ra[1:]:
            t = pd.read_csv(self.rootpath + "/GraduationDesign/语料库/客服语料/整理后/" + str(i) + ".csv")
            # 纵向拼接df和t
            df = pd.concat([df, t], ignore_index=True)
        df.to_csv(self.rootpath + "/GraduationDesign/语料库/客服语料/整理后/[{}-{}].csv".format(ra[0], ra[-1]), index=False)
        print("处理完成，生成文件：[{}-{}].csv，此文件共{}行".format(ra[0], ra[-1], len(df)))

processor = Processor("D:")
# for i in range(1, 7):
#     processor.generateMd(i)
# processor.concatCsv([1, 2, 3, 4, 5, 6])
# processor.generateMd(7)