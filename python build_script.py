import os
import json
import shutil
import subprocess
from datetime import datetime


def log(message):
    """Логирует сообщения с отметкой времени."""
    print(f"{datetime.now()}: {message}")


def clone_repository(repo_url):
    """Клонирует репозиторий по указанному URL."""
    log(f"Клонирование репозитория: {repo_url}")
    subprocess.run(["git", "clone", repo_url], check=True)


def clean_directory(root_dir, source_path):
    """Удаляет все директории в корне, кроме указанной."""
    log(f"Очистка директории: {root_dir}, оставляя только {source_path}")
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path) and item != source_path:
            shutil.rmtree(item_path)
            log(f"Удалена директория: {item_path}")


def create_version_file(source_dir, version):
    """Создает файл version.json с информацией о версии и файлах."""
    log(f"Создание файла version.json в директории: {source_dir}")
    files = [f for f in os.listdir(source_dir) if f.endswith(('.py', '.js', '.sh'))]

    version_info = {
        "name": "hello world",
        "version": version,
        "files": files
    }

    version_file_path = os.path.join(source_dir, "version.json")
    with open(version_file_path, 'w') as version_file:
        json.dump(version_info, version_file, indent=4)

    log(f"Файл version.json создан: {version_file_path}")


def create_archive(source_dir):
    """Упаковывает исходный код и файл version.json в архив."""
    archive_name = os.path.basename(source_dir) + datetime.now().strftime("%d%m%Y") + ".zip"
    log(f"Создание архива: {archive_name}")

    shutil.make_archive(os.path.splitext(archive_name)[0], 'zip', os.path.dirname(source_dir),
                        os.path.basename(source_dir))
    log(f"Архив создан: {archive_name}")


def main(repo_url, source_path, version):
    """Основная функция для выполнения всех шагов."""
    try:
        # Клонирование репозитория
        clone_repository(repo_url)

        # Получение имени директории репозитория
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        root_dir = os.path.join(os.getcwd(), repo_name)

        # Очистка директории
        clean_directory(root_dir, source_path)

        # Путь к исходному коду
        source_dir = os.path.join(root_dir, source_path)

        # Создание файла version.json
        create_version_file(source_dir, version)

        # Создание архива
        create_archive(source_dir)

        log("Скрипт выполнен успешно.")

    except Exception as e:
        log(f"Ошибка: {e}")


if __name__ == "__main__":
    # Пример использования
    repo_url = "https://github.com/paulbouwer/hello-kubernetes.git"
    source_path = "src/app"
    version = "25.3000"

    main(repo_url, source_path, version)
