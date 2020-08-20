#!/usr/bin/env python3
import pathlib
import re
import sys


parent = pathlib.Path(__file__).parent
path = parent / sys.argv[1]


def get_args():
    path = parent / path
    if not path:
        print('file path is required')
        sys.exit(1)


def main():
    lines = []
    with open(path) as f:
        orig_lines = f.readlines()
        match_lines = map(match_pattern, orig_lines)
        lines = list(filter(lambda line: line is not None, match_lines))

    obj = {
        'youtube': convert_for_youtube,
        'anchor': convert_for_anchor,
    }
    for media_type in ['youtube', 'anchor']:
        print(media_type)
        print(obj[media_type](lines))
        create_file(
            media_type,
            obj[media_type](lines),
        )


def match_pattern(content):
    pattern = '^\*\s(.*)$'
    match_obj = re.match(pattern, content)
    if match_obj is not None:
        return match_obj.groups()[0]

    return None


def convert_for_youtube(lines):
    new_lines = []
    count = 1
    for line in lines:
        if line.startswith('http'):
            new_lines.append(line + '\n')
        else:
            new_lines.append(f'{str(count)}. {line}')
            count += 1

    return new_lines


def convert_for_anchor(lines):
    new_lines = []
    title = ''
    for line in lines:
        if line.startswith('http'):
            new_lines.append('<li><a href="{}">{}</a></li>'.format(
                line,
                title,
            ))
        else:
            title = line

    return new_lines


def create_file(media_type, lines):
    file_dir = parent / path.stem
    file_dir.mkdir(exist_ok=True)
    file_path = file_dir / media_type
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))


main()
