import json
import os
import re
import zipfile
from argparse import ArgumentParser
from typing import Union


class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small containers on single lines."""

    CONTAINER_TYPES = (list, tuple, dict)
    """Container datatypes include primitives or other containers."""

    MAX_WIDTH = 70
    """Maximum width of a container that might be put on a single line."""

    MAX_ITEMS = 2
    """Maximum number of items in container that might be put on single line."""

    INDENTATION_CHAR = " "

    def __init__(self, *args, **kwargs):
        # using this class without indentation is pointless
        if kwargs.get("indent") is None:
            kwargs.update({"indent": 4})
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o):
        """Encode JSON object *o* with respect to single line lists."""
        if isinstance(o, (list, tuple)):
            if self._put_on_single_line(o):
                return "[" + ", ".join(self.encode(el) for el in o) + "]"
            else:
                self.indentation_level += 1
                output = [self.indent_str + self.encode(el) for el in o]
                self.indentation_level -= 1
                return "[\n" + ",\n".join(output) + "\n" + self.indent_str + "]"
        elif isinstance(o, dict):
            if o:
                if self._put_on_single_line(o):
                    return "{" + ", ".join(f"{self.encode(k)}: {self.encode(el)}" for k, el in o.items()) + "}"
                else:
                    self.indentation_level += 1
                    output = [self.indent_str + f"{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()]
                    self.indentation_level -= 1
                    return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"
            else:
                return "{}"
        elif isinstance(o, float):  # Use scientific notation for floats, where appropiate
            return format(o, "g")
        elif isinstance(o, str):  # escape newlines
            o = o.replace("\n", "\\n")
            return f'"{o}"'
        else:
            return json.dumps(o)

    def iterencode(self, o, **kwargs):
        """Required to also work with `json.dump`."""
        return self.encode(o)

    def _put_on_single_line(self, o):
        return self._primitives_only(o) and len(o) <= self.MAX_ITEMS and len(str(o)) - 2 <= self.MAX_WIDTH

    def _primitives_only(self, o: Union[list, tuple, dict]):
        if isinstance(o, (list, tuple)):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o)
        elif isinstance(o, dict):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o.values())

    @property
    def indent_str(self) -> str:
        return self.INDENTATION_CHAR * (self.indentation_level * self.indent)


def natural_sort_key(s, _nsre=re.compile(r"(\d+)")):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]


def keep_line_feed_only(s):
    return s.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def filter_name_list(name_list, judging_mode='standard', in_dir='', out_dir='', ext=''):
    file_list = []
    in_regex = fr'^{in_dir}(.+?){ext}$'
    for name in name_list:
        m = re.search(in_regex, name)
        if m:
            found = m.group(1)
            file_list.append(found)

    test_case_list = []
    if judging_mode == 'standard':
        for file_name in file_list:
            if f"{in_dir}{file_name}{ext}" in name_list and f"{out_dir}{file_name}{ext}" in name_list:
                test_case_list.append((f"{in_dir}{file_name}{ext}", f"{out_dir}{file_name}{ext}"))
    else:
        for file_name in file_list:
            if f"{in_dir}{file_name}{ext}" in name_list:
                test_case_list.append((f"{in_dir}{file_name}{ext}",))
    return test_case_list


def main(arguments):
    # some variables, need to check the source zip file before execution
    in_dir = 'in/'
    out_dir = 'out/'
    # change this ext if the ext of in out files changes, if no ext, please use empty string
    ext = '.txt'

    test_case_dir = arguments.output
    zip_file = arguments.file
    judging_mode = arguments.mode
    try:
        zip_file = zipfile.ZipFile(zip_file, "r")
    except zipfile.BadZipFile:
        print("ERROR: bad zip file")
        return

    name_list = sorted(zip_file.namelist())
    test_case_list = filter_name_list(name_list, judging_mode=judging_mode, in_dir=in_dir, out_dir=out_dir, ext=ext)
    if not test_case_list:
        print("ERROR: empty file")
        return

    try:
        os.mkdir(test_case_dir)
    except Exception:
        print('ERROR: output dir exists ' + test_case_dir)
        return

    new_test_case_list = []
    for item in test_case_list:
        in_item = item[0]
        in_regex = fr'^{in_dir}(.+?){ext}$'
        m = re.search(in_regex, in_item)
        item_name = m.group(1)

        content = keep_line_feed_only(zip_file.read(f"{in_item}"))
        in_file_name = f"{item_name}.in"
        new_test_case_list.append(in_file_name)
        with open(os.path.join(test_case_dir, in_file_name), "wb") as f:
            f.write(content)

        if judging_mode == 'standard':
            content = keep_line_feed_only(zip_file.read(f"{in_item}"))
            out_file_name = f"{item_name}.out"
            new_test_case_list.append(out_file_name)
            with open(os.path.join(test_case_dir, out_file_name), "wb") as f:
                f.write(content)

    test_case_list = sorted(new_test_case_list, key=natural_sort_key)
    test_case_info = {"mode": judging_mode, "test_cases": []}

    if judging_mode == 'standard':
        # ["1.in", "1.out", "2.in", "2.out"] => [("1.in", "1.out"), ("2.in", "2.out")]
        test_case_list = zip(*[test_case_list[i::2] for i in range(2)])
        for index, item in enumerate(test_case_list):
            data = {
                "in": item[0],
                "out": item[1],
            }
            test_case_info["test_cases"].append(data)
    else:
        for index, item in enumerate(test_case_list):
            data = {"in": item}
            test_case_info["test_cases"].append(data)

    encoder = CompactJSONEncoder()
    with open(os.path.join(test_case_dir, "info.json"), "w", encoding="utf-8") as f:
        f.write(encoder.encode(test_case_info))

    print('Done! Please check the destination directory.')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', type=str, dest='file', default='', help='atcoder testcase zip file')
    parser.add_argument('-m', type=str, dest='mode', default='standard', help='judging mode')
    parser.add_argument('-o', type=str, dest='output', default='', help='output dir')
    args = parser.parse_args()
    main(args)
