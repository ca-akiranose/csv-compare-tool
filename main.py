import argparse
import csv
import os
import time
from itertools import zip_longest

_INPUT_FILE_DIR =  home_dir = os.path.expanduser('~') + "/Downloads/"


def main():
    parser = argparse.ArgumentParser(description='2つのCSVファイルを比較するスクリプト')
    parser.add_argument('file1', help='1つ目のCSVファイルの名前')
    parser.add_argument('file2', help='2つ目のCSVファイルの名前')
    args = parser.parse_args()

    file1, file2 = _INPUT_FILE_DIR + args.file1, _INPUT_FILE_DIR + args.file2

    start_time = time.time()
    print(f"CSVファイル比較を開始します。\n\n対象ファイル: \n- {file1}\n- {file2}")

    result = True
    different_order_count = 0

    try:
        with open(file1, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)

        with (
            open(file1, "r", encoding="utf-8") as f1,
            open(file2, "r", encoding="utf-8") as f2,
        ):
            reader1, reader2 = csv.reader(f1), csv.reader(f2)

            # see: enumerate https://docs.python.org/ja/3/library/functions.html#enumerate
            # see: zip_longest https://docs.python.org/ja/3/library/itertools.html#itertools.zip_longest
            for idx, (row1, row2) in enumerate(zip_longest(reader1, reader2), start=1):
                if row1 is None or row2 is None:
                    print(f"CSVファイルの行数が一致しません。行番号 {idx} 付近を確認してください。")
                    return

                for idx1, (row1_elem, row2_elem) in enumerate(zip(row1, row2)):
                    if row1_elem != row2_elem:
                        if ", " in row1_elem and ", " in row2_elem:
                            sp_row1_elem, sp_row2_elem = row1_elem.split(", "), row2_elem.split(", ")
                            if set(sp_row1_elem) == set(sp_row2_elem):
                                different_order_count += 1
                                # print(f"\n[{idx}行目,{idx1}列目({header[idx1]})] 順番は異なりますが、要素の内容は一致しています。")
                                continue

                        if "," in row1_elem and "," in row2_elem:
                            sp_row1_elem, sp_row2_elem = row1_elem.split(","), row2_elem.split(",")
                            if set(sp_row1_elem) == set(sp_row2_elem):
                                different_order_count += 1
                                # print(f"\n[{idx}行目,{idx1}列目({header[idx1]})] 順番は異なりますが、要素の内容は一致しています。")
                                continue

                        print(f"\n[{idx}行目,{idx1}列目({header[idx1]})] 情報が一致しません。")
                        print(f"[file1]: {row1_elem}")
                        print(f"[file2]: {row2_elem}")
                        result = False

        if result:
            print("\n2つのCSVの情報は全て一致しています。")
            if different_order_count > 0:
                print(f"ただし、順番が異なるデータが {different_order_count} 件あります。")
        else:
            print("\n2つのCSVの情報に差異があります。")

    except FileNotFoundError as e:
        print(f"ファイルが見つかりません。ファイル名: {e.filename}")
    finally:
        print(f"\n処理時間: {time.time() - start_time:.5f} 秒")


if __name__ == "__main__":
    main()
