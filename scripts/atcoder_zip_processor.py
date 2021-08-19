import hashlib
import json
import os
import re
import zipfile
from argparse import ArgumentParser


def natural_sort_key(s, _nsre=re.compile(r"(\d+)")):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]


def filter_name_list(name_list, spj=0, in_dir='', out_dir='', ext=''):
    file_list = []
    in_regex = fr'^{in_dir}(.+?){ext}$'
    for name in name_list:
        m = re.search(in_regex, name)
        if m:
            found = m.group(1)
            file_list.append(found)

    test_case_list = []
    if spj:
        for file_name in file_list:
            if f"{in_dir}{file_name}{ext}" in name_list:
                test_case_list.append((f"{in_dir}{file_name}{ext}",))
    else:
        for file_name in file_list:
            if f"{in_dir}{file_name}{ext}" in name_list and f"{out_dir}{file_name}{ext}" in name_list:
                test_case_list.append((f"{in_dir}{file_name}{ext}", f"{out_dir}{file_name}{ext}"))
    return test_case_list


def main(arguments):
    # some variables, need to check the source zip file before execution
    in_dir = 'in/'
    out_dir = 'out/'
    ext = '.txt'

    test_case_dir = arguments.output
    zip_file = arguments.file
    spj = arguments.spj
    try:
        zip_file = zipfile.ZipFile(zip_file, "r")
    except zipfile.BadZipFile:
        print("bad zip file")
        return

    name_list = zip_file.namelist()
    test_case_list = filter_name_list(name_list, spj=spj, in_dir=in_dir, out_dir=out_dir, ext=ext)
    if not test_case_list:
        print("empty file")
        return

    os.mkdir(test_case_dir)

    size_cache = {}
    md5_cache = {}

    prefix = 0
    new_test_case_list = []
    for item in test_case_list:
        prefix += 1

        in_item = item[0]
        content = zip_file.read(f"{in_item}").replace(b"\r\n", b"\n")
        in_file_name = f"{prefix}.in"
        new_test_case_list.append(in_file_name)
        size_cache[in_file_name] = len(content)
        with open(os.path.join(test_case_dir, in_file_name), "wb") as f:
            f.write(content)

        if not spj:
            out_item = item[1]
            content = zip_file.read(f"{out_item}").replace(b"\r\n", b"\n")
            out_file_name = f"{prefix}.out"
            new_test_case_list.append(out_file_name)
            size_cache[out_file_name] = len(content)
            md5_cache[out_file_name] = hashlib.md5(content.rstrip()).hexdigest()
            with open(os.path.join(test_case_dir, out_file_name), "wb") as f:
                f.write(content)

    test_case_list = sorted(new_test_case_list, key=natural_sort_key)
    test_case_info = {"spj": spj, "test_cases": {}}
    info = []

    if spj:
        for index, item in enumerate(test_case_list):
            data = {"input_name": item, "input_size": size_cache[item]}
            info.append(data)
            test_case_info["test_cases"][str(index + 1)] = data
    else:
        # ["1.in", "1.out", "2.in", "2.out"] => [("1.in", "1.out"), ("2.in", "2.out")]
        test_case_list = zip(*[test_case_list[i::2] for i in range(2)])
        for index, item in enumerate(test_case_list):
            data = {
                "stripped_output_md5": md5_cache[item[1]],
                "input_size": size_cache[item[0]],
                "output_size": size_cache[item[1]],
                "input_name": item[0],
                "output_name": item[1],
            }
            info.append(data)
            test_case_info["test_cases"][str(index + 1)] = data

    with open(os.path.join(test_case_dir, "info"), "w", encoding="utf-8") as f:
        f.write(json.dumps(test_case_info, indent=4))

    print('Done! Please check the destination directory.')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', type=str, dest='file', default='', help='atcoder testcase zip file')
    parser.add_argument('-s', type=int, dest='spj', default=0, help='special judge (0 or 1)')
    parser.add_argument('-o', type=str, dest='output', default='', help='output dir')
    args = parser.parse_args()
    main(args)
