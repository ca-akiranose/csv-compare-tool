import csv
import time
from itertools import zip_longest

_INPUT_FILE_DIR = "input/"
_FILE1 = "1.csv"
_FILE2 = "2.csv"


def main():
    start_time = time.time()
    print(f"CSVファイル比較を開始します。\n\n対象ファイル: \n- {_FILE1}\n- {_FILE2}\n")

    try:
        with (
            open(_INPUT_FILE_DIR + _FILE1, "r", encoding="utf-8") as f1,
            open(_INPUT_FILE_DIR + _FILE2, "r", encoding="utf-8") as f2,
        ):
            reader1, reader2 = csv.reader(f1), csv.reader(f2)

            # see: enumerate https://docs.python.org/ja/3/library/functions.html#enumerate
            # see: zip_longest https://docs.python.org/ja/3/library/itertools.html#itertools.zip_longest
            for idx, (row1, row2) in enumerate(zip_longest(reader1, reader2), start=1):
                if row1 is None or row2 is None:
                    print(f"CSVファイルの行数が一致しません。行番号 {idx} 付近を確認してください。")
                    return

                if row1 != row2:
                    print(f"CSVファイルの {idx} 行目の情報が一致しません。")
                    print(f"\n[{_FILE1}]\n{row1}")
                    print(f"\n[{_FILE2}]\n{row2}")
                    return

            print("2つのCSVの情報は全て一致しています。")
    except FileNotFoundError as e:
        print(f"ファイルが見つかりません。ファイル名: {e.filename}")
    finally:
        print(f"\n処理時間: {time.time() - start_time:.5f} 秒")


if __name__ == "__main__":
    main()
