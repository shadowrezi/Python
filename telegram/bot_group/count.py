from pathlib import Path
# from asyncio import run


async def get_path(path, extensions):
    files = []

    for one_file in Path(path).rglob('*' + extensions):
        if 'venv' not in one_file.parts:
            files.append(one_file)

    return files


async def count_pages_of_project():
    files = await get_path('\\Users\\ShadowRaze\\Documents\\Python\\telegram\\telegram_bot', '.py')
    all_lines = []
    lines = []

    for file in files:
        for line in open(file, 'r', encoding='utf-8').readlines():
            lines.append(1 if line != '\n' else 0)
            all_lines.append(1)

    return [sum(lines), sum(all_lines)]
