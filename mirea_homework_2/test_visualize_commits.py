import unittest
from unittest.mock import patch, MagicMock
import os
import subprocess
from graphviz import Digraph
import yaml
from datetime import datetime
from visualize_commits import get_commits_by_tag, build_dependency_graph, save_graph, load_config

"""
python -m unittest test_visualize_commits.py
"""

class TestGitVisualizer(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_commits_by_tag(self, mock_run):
        # Подготовим mock данных
        mock_run.return_value = MagicMock(stdout="abc123 1609459200\nxyz789 1609545600\n", returncode=0)

        # Вызовем функцию
        repo_path = "mock_repo"
        tag_name = "v1.0"
        commits = get_commits_by_tag(repo_path, tag_name)

        # Проверяем результат
        self.assertEqual(commits[0][0], "xyz789")
        self.assertEqual(commits[1][0], "abc123")
        self.assertEqual(commits[0][1], "2021-01-02 00:00:00")  # Дата для 'xyz789'
        self.assertEqual(commits[1][1], "2021-01-01 00:00:00")  # Дата для 'abc123'

    @patch("subprocess.run")
    def test_build_dependency_graph(self, mock_run):
        """Тестируем создание графа зависимостей"""
        # Моки для получения коммитов и их родительских коммитов
        mock_run.return_value = MagicMock(returncode=0, stdout="abc123 xyz789")

        # Подготовка тестовых данных
        commits = [("abc123", "2021-01-01 00:00:00"), ("xyz789", "2021-01-02 00:00:00")]
        repo_path = "/path/to/repo"

        # Построение графа
        graph = build_dependency_graph(commits, repo_path)

        # Проверяем, что граф был построен
        self.assertIsInstance(graph, Digraph)
        self.assertIn("Commit: abc123", graph.source)
        self.assertIn("Commit: xyz789", graph.source)
        self.assertIn("xyz789", graph.source)  # Проверяем, что есть связь

    @patch("graphviz.Digraph.render")
    def test_save_graph(self, mock_render):
        """Тестируем сохранение графа в файл"""
        graph = Digraph()
        output_file = "output"

        # Вызов функции
        save_graph(graph, output_file)

        # Проверка, что функция render была вызвана с правильными параметрами
        mock_render.assert_called_with(output_file, format="png")

    def test_load_config(self):
        """Тестируем загрузку конфигурации из файла"""
        # Создаем временный файл с конфигурацией
        config_data = {
            "repository_path": "/path/to/repo",
            "tag_name": "v1.0",
            "graph_output_path": "output"
        }
        with open("test_config.yaml", "w") as file:
            yaml.dump(config_data, file)

        # Загружаем конфигурацию
        config = load_config("test_config.yaml")

        # Проверяем корректность данных
        self.assertEqual(config["repository_path"], "/path/to/repo")
        self.assertEqual(config["tag_name"], "v1.0")
        self.assertEqual(config["graph_output_path"], "output")

        # Удаляем временный файл
        os.remove("test_config.yaml")


if __name__ == "__main__":
    unittest.main()
