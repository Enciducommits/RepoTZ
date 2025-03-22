import os
import shutil
import subprocess
import stat
from datetime import datetime
import time


def log(message):
    """Логирует сообщение."""
    print(f"{datetime.now()}: {message}")


def create_archive(source_dir):
    """Упаковывает исходный код и файл version.json в архив."""
    archive_name = os.path.basename(source_dir) + datetime.now().strftime("%d%m%Y") + ".zip"
    log(f"Создание архива: {archive_name}")

    shutil.make_archive(os.path.splitext(archive_name)[0], 'zip', os.path.dirname(source_dir),
                        os.path.basename(source_dir))
    log(f"Архив создан: {archive_name}")


def remove_readonly(func, path, excinfo):
    """Обработчик ошибок для удаления файлов с ограниченными правами."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repository(repo_url):
    """Клонирует репозиторий по указанному URL."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")

    if os.path.exists(repo_name):
        log(f"Директория {repo_name} уже существует. Удаление...")
        try:
            shutil.rmtree(repo_name, onerror=remove_readonly)  # Удаляем существующую директорию
            time.sleep(1)  # Добавляем задержку перед клонированием
        except Exception as e:
            log(f"Ошибка при удалении директории: {e}")
            return

    log(f"Клонирование репозитория: {repo_url}")
    subprocess.run(["git", "clone", repo_url], check=True)


def clean_directory(root_dir, source_path):
    """Очищает директорию от старых файлов."""
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path) and item != os.path.basename(source_path):
            log(f"Удаление директории: {item_path}")
            try:
                shutil.rmtree(item_path, onerror=remove_readonly)
            except Exception as e:
                log(f"Ошибка при удалении директории {item_path}: {e}")


def create_version_file(source_dir, version):
    """Создает файл version.json с указанной версией."""
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)

    files_list = [f for f in os.listdir(source_dir) if f.endswith(('.py', '.js', '.sh'))]
    version_file_path = os.path.join(source_dir, "version.json")

    version_content = {
        "name": "hello world",
        "version": version,
        "files": files_list
    }

    with open(version_file_path, 'w') as version_file:
        version_file.write(str(version_content).replace("'", '"'))
        log(f"Создан файл version.json в директории: {source_dir}")


def main(repo_url, source_path, version):
    """Основная функция для выполнения всех шагов."""
    try:
        clone_repository(repo_url)

        repo_name = repo_url.split("/")[-1].replace(".git", "")
        root_dir = os.path.join(os.getcwd(), repo_name)

        clean_directory(root_dir, source_path)

        source_dir = os.path.join(root_dir, source_path)

        create_version_file(source_dir, version)

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
