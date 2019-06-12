"""Read excel database."""
import os
import json
import pandas as pd


GB = "GEN11_MASTER_TCP_GB_NEW.xlsx"
EXCEL_DIR = r'Z:\Engineering\01.OnStar\11.Flashing\01.Reflash\Excel Database'


def main():
    """Main."""
    if not os.path.exists("reader_output"):
        os.mkdir("reader_output")
    df = pd.read_excel(os.path.join(EXCEL_DIR, GB), sheet_name=None, dtype=str)
    unused = []
    used = []
    unused_STIDs = {}
    used_STIDs = {}
    for sheet_name in df.keys():
        if sheet_name[-1] == 'B':
            continue

        for _, row in df[sheet_name].iterrows():
            if not pd.isnull(row['STID']):
                if pd.isnull(row['#']) and pd.isnull(row['LG Contact']) and \
                   pd.isnull(row['CCM SW']) and pd.isnull(row['CCM HW']) and \
                   pd.isnull(row['VIM SW']) and pd.isnull(row['VIM HW']):
                    unused.append(row)
                    unused_STIDs[row['STID']] = 1
                else:
                    used.append(row)
                    used_STIDs[row['STID']] = 1

    # Output json files
    with open('reader_output/unused_GB.txt', 'w') as file:
        json.dump(unused_STIDs, file)
    with open('reader_output/used_GB.txt', 'w') as file:
        json.dump(used_STIDs, file)

    # Sample Output on Excel Files
    df_unused = pd.DataFrame(unused, columns=df['MY20Gen11CN_GB'].columns)
    df_unused.to_excel("reader_output/unused_GB.xlsx")
    df_used = pd.DataFrame(used, columns=df['MY20Gen11CN_GB'].columns)
    df_used.to_excel("reader_output/used_GB.xlsx")


if __name__ == "__main__":
    main()
