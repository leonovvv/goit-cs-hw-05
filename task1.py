import os
import asyncio
import shutil
import logging
from argparse import ArgumentParser
from pathlib import Path

# Налаштування логування
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder: Path, output_folder: Path):
    """Рекурсивно читає всі файли у вихідній папці."""
    try:
        for root, _, files in os.walk(source_folder):
            tasks = []
            for file in files:
                file_path = Path(root) / file
                tasks.append(copy_file(file_path, output_folder))
            await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")

async def copy_file(file_path: Path, output_folder: Path):
    """Копіює файл у відповідну підпапку цільової папки на основі розширення."""
    try:
        extension = file_path.suffix[1:] or "no_extension"
        target_folder = output_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / file_path.name

        # Виконання копіювання файлу
        shutil.copy2(file_path, target_file)
        print(f"Copied {file_path} to {target_file}")
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")

if __name__ == "__main__":
    # Налаштування парсера аргументів командного рядка
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output", type=str, help="Шлях до цільової папки")
    args = parser.parse_args()

    # Ініціалізація шляхів
    source_folder = Path(args.source)
    output_folder = Path(args.output)

    if not source_folder.is_dir():
        print(f"Error: Source folder '{source_folder}' не існує або не є директорією.")
        exit(1)

    # Запуск асинхронного сортування
    asyncio.run(read_folder(source_folder, output_folder))
