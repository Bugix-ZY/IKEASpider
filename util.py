import pandas as pd
from typing import List


def write_list_to_csv(data: List, path: str, header: str):
    print("\nWrite to:", path)
    df = pd.DataFrame(data, columns=[header])
    df.to_csv(path, index=False)
    print("Done.")


def append_list_to_csv(data: List, path: str):
    print("Append to:", path)
    df = pd.DataFrame(data)
    df.to_csv(path, mode='a', index=False, header=False)
    print("Done.\n")


if __name__ == '__main__':
    l = ['google.com', 'youtube.com', 'amazon.com']
    write_list_to_csv(l, 'test.csv', 'url')
