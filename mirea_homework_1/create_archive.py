import tarfile
import os

# Путь к директории, содержащей файлы и папки для архивации
vfs_dir = "test_vfs"

# Проверяем, существует ли директория
if not os.path.exists(vfs_dir):
    print(f"Директория {vfs_dir} не найдена. Убедитесь, что она существует.")
else:
    # Создаём новый tar-архив
    with tarfile.open("vfs_new.tar", "w") as new_tar:
        for root, dirs, files in os.walk(vfs_dir):
            for name in files:
                filepath = os.path.join(root, name)
                # Убираем префикс 'test_vfs' для корректной структуры
                arcname = os.path.relpath(filepath, start=vfs_dir)
                new_tar.add(filepath, arcname=arcname)

    print("Создан новый архив: vfs_new.tar")