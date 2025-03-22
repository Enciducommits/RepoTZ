import json
import argparse
from packaging import version
from packaging.version import Version
from typing import List, Dict
import random

random.seed(42)

def generate_versions(template: str) -> List[str]:
    parts = template.split('.')
    generated_versions = []
    for _ in range(2):
        new_version = []
        for part in parts:
            if part == '*':
                new_version.append(str(random.randint(0, 255)))
            else:
                new_version.append(part)
        generated_versions.append(".".join(new_version))
    return generated_versions

def read_config(config_file: str) -> Dict[str, str]:
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Ошибка: Файл конфигурации '{config_file}' не найден.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный JSON формат в файле '{config_file}'.")
        exit(1)

def filter_older_versions(versions: List[str], target_version: str) -> List[str]:
    older_versions = []
    try:
        target = version.parse(target_version)
        for v in versions:
            try:
                ver = version.parse(v)
                if ver < target:
                    older_versions.append(v)
            except version.InvalidVersion as e:
                print(f"Предупреждение: Некорректный формат версии '{v}', пропущено.")
    except version.InvalidVersion as e:
        print(f"Ошибка: Некорректный формат версии '{target_version}': {e}")
        return []
    return older_versions

def main():
    parser = argparse.ArgumentParser(description="Генератор и фильтратор номеров версий.")
    parser.add_argument("version", help="Номер версии продукта для сравнения.")
    parser.add_argument("config_file", help="Имя конфигурационного файла с шаблонами версий.")
    args = parser.parse_args()

    version_number = args.version
    config_file_path = args.config_file

    config = read_config(config_file_path)

    all_versions = []
    for service, template in config.items():
        versions = generate_versions(template)
        all_versions.extend(versions)

    unique_versions = []
    for v in all_versions:
        try:
            ver = version.parse(v)
            if ver not in unique_versions:
                unique_versions.append(ver)
        except version.InvalidVersion:
            print(f"Предупреждение: Некорректный формат версии '{v}', пропущено.")

    unique_versions.sort()

    sorted_versions = [str(v) for v in unique_versions]

    print("Все сгенерированные и отсортированные номера версий:")
    for v in sorted_versions:
        print(v)

    older_versions = filter_older_versions(sorted_versions, version_number)
    print("\nНомера версий старее, чем {}:".format(version_number))
    for v in older_versions:
        print(v)

if __name__ == "__main__":
    main()
