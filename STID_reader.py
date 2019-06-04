import os
import time
import json
import numpy as np
import pandas as pd


GB = "GEN11_MASTER_TCP_GB_NEW.xlsx"
EXCEL_DIR = 'Z:\\Engineering\\01.OnStar\\11.Flashing\\01.Reflash\\Excel Database'


def main():
    if not os.path.exists("output"):
        os.mkdir("output")
    df = pd.read_excel(EXCEL_DIR + GB, sheet_name=None, dtype=str)
    unused = []
    used = []
    unused_STIDs = {}
    used_STIDs = {}
    for sheet_name in df.keys():
        if sheet_name[-1] is not 'B':
            continue

        for index, row in df[sheet_name].iterrows():
            if not pd.isnull(row['STID']):
                if pd.isnull(row['#']) and pd.isnull(row['CCM SW']) and pd.isnull(row['CCM HW']) and pd.isnull(row['VIM SW']) and pd.isnull(row['VIM HW']):
                    unused.append(row)
                    unused_STIDs[row['STID']] = 1
                else:
                    used.append(row)
                    used_STIDs[row['STID']] = 1

    # Output json files
    with open('output/unused_GB.txt', 'w') as f:
        json.dump(unused_STIDs, f)
    with open('output/used_GB.txt', 'w') as f:
        json.dump(used_STIDs, f)
    print(len(used_STIDs))

    # Sample Output on Excel Files
    df_unused = pd.DataFrame(unused, columns=df['MY20Gen11CN_GB'].columns)
    df_unused.to_excel("output/unused_GB.xlsx")
    df_used = pd.DataFrame(used, columns=df['MY20Gen11CN_GB'].columns)
    df_used.to_excel("output/used_GB.xlsx")


if __name__ == "__main__":
    main()
