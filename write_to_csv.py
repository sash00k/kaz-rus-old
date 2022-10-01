from pathlib import Path
from clean_text import light_clean
from group import Group


def write(group: Group, text: str | list, text_type: str, writing_type='strings') -> None:
    match writing_type:
        case 'strings':
            for text_item in text:
                text_item = light_clean(text_item)
                group.file.write(','.join([str(group.domain),
                                           str(group.group_type),
                                           text_type,
                                           '"'+text_item + '"']) + '\n')
        case 'string':
            text = light_clean(text)
            group.file.write(','.join([str(group.domain),
                                       str(group.group_type),
                                       text_type,
                                       '"' + text + '"']) + '\n')


def write_header(group: Group) -> None:
    group.file.write(','.join(['group', 'group_type', 'text_type', 'text']) + '\n')
