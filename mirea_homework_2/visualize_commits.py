import os
import subprocess
from datetime import datetime
from typing import List, Tuple
from graphviz import Digraph
import yaml

def get_commits_by_tag(repo_path: str, tag_name: str) -> List[Tuple[str, str]]:
    """
    Получает список коммитов для указанного тега в репозитории.
    """
    git_command = [
        "git",
        "-C",
        repo_path,
        "log",
        "--pretty=format:%H %ct",  # Получаем хеш коммита и время
        tag_name,
    ]
    result = subprocess.run(git_command, stdout=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise Exception(f"Ошибка при выполнении git команды: {result.stderr}")

    commits = result.stdout.splitlines()
    commit_data = [
        (
            c.split()[0],  # Хеш коммита
            datetime.utcfromtimestamp(int(c.split()[1])).strftime("%Y-%m-%d %H:%M:%S"),  # Преобразуем метку времени в дату
        )
        for c in commits
    ]
    return commit_data[::-1]  # Возвращаем коммиты в обратном порядке (по порядку, от старого к новому)

def build_dependency_graph(commits: List[Tuple[str, str]], repo_path: str) -> Digraph:
    """
    Строит граф зависимостей для коммитов.
    """
    dot = Digraph(comment="Git Commit Dependencies")  # Создаем объект для графа

    # Для каждого коммита добавляем узел в граф
    for i, (commit, date) in enumerate(commits):
        dot.node(str(i), f"Commit: {commit}\nDate: {date}")

        # Формируем команду для получения родительских коммитов
        git_command = [
            "git",
            "-C",
            repo_path,
            "log",
            "--pretty=format:%H",
            "--parents",  # Показываем родительские коммиты
            commit,
        ]
        result = subprocess.run(git_command, stdout=subprocess.PIPE, text=True)

        if result.returncode != 0:
            raise Exception(f"Ошибка при получении родительских коммитов для {commit}")

        parent_commits = result.stdout.split()

        # Добавляем ребра между коммитами и их родителями
        for parent in parent_commits[1:]:  # Пропускаем сам коммит
            parent_index = next((index for index, c in enumerate(commits) if c[0] == parent), None)
            if parent_index is not None:
                dot.edge(str(parent_index), str(i))  # Добавляем ребро между коммитом и родителем

    return dot  # Возвращаем построенный граф

def save_graph(graph: Digraph, output_file: str) -> None:
    """
    Сохраняет граф в файл в формате PNG.
    """
    graph.render(output_file, format="png")  # Сохраняем граф в формате PNG
    print(f"Граф успешно сохранён в файл {output_file}.png")

def load_config(config_file: str) -> dict:
    """
    Загружает конфигурацию из YAML файла.
    """
    with open(config_file, "r") as file:
        return yaml.safe_load(file)  # Загружаем конфигурацию из YAML файла

def main(config_file: str) -> None:
    """
    Основная логика программы:
    - Загружает настройки из конфигурационного файла,
    - Получает коммиты для указанного тега,
    - Строит граф зависимостей и сохраняет его в файл.
    """
    config = load_config(config_file)
    repo_path = config["repository_path"]
    tag_name = config["tag_name"]
    graph_output_path = config["graph_output_path"]

    # Проверяем, существует ли указанный путь к репозиторию
    if not os.path.exists(repo_path):
        print(f"Ошибка: Путь к репозиторию '{repo_path}' не существует.")
        return

    # Получаем коммиты для указанного тега
    commits = get_commits_by_tag(repo_path, tag_name)

    # Если коммиты не найдены, выводим сообщение
    if not commits:
        print(f"Не найдено коммитов для тега {tag_name}")
        return

    # Строим граф зависимостей коммитов
    graph = build_dependency_graph(commits, repo_path)
    # Сохраняем граф в файл
    save_graph(graph, graph_output_path)

if __name__ == "__main__":
    config_file = "config.yaml"  # Путь к вашему конфигурационному файлу
    main(config_file)
