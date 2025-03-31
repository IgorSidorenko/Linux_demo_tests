import subprocess
import os
import pytest
import time

"""
Инструкция по запуску:
1. Установите зависимости: pip install pytest
2. Запустите: pytest -v test_linux_demo.py
"""

# Тест 1: Проверка работы с файловой системой
def test_file_operations(tmp_path):
    """Создание, запись и проверка файла"""
    test_file = tmp_path / "demo.txt"

    # Создаем файл и записываем данные
    test_file.write_text("Igor Sidorenko Python QA Automation!")

    # Проверяем существование файла
    assert os.path.exists(test_file), "Файл должен быть создан"

    # Проверяем содержимое файла
    with open(test_file, 'r') as f:
        content = f.read()
    assert "QA Automation" in content, "Файл содержит неверные данные"

# Тест 2: Проверка работы процессов
def test_process_management():
    """Запуск и проверка системных процессов"""
    # Запускаем фоновый процесс
    process = subprocess.Popen(['sleep', '2'])

    # Проверяем статус процесса
    assert process.poll() is None, "Процесс должен быть запущен"

    # Ждем завершения и проверяем статус
    time.sleep(3)
    assert process.poll() == 0, "Процесс должен завершиться успешно"

#Тест 3: Анализ логов (параметризованный тест)
@pytest.mark.parametrize("pattern,expected_count", [
    ("INFO", 2),
    ("ERROR", 1),
    ("WARNING", 0),
])
def test_log_analysis(tmp_path, pattern, expected_count):
    """Проверка анализа логов с разными параметрами"""
    log_content = """
    [INFO] System started
    [ERROR] Disk full
    [INFO] User logged in
    """
    log_file = tmp_path / "app.log"
    log_file.write_text(log_content)

    # Запускаем grep для поиска паттерна
    result = subprocess.run(
        ['grep', '-c', pattern, str(log_file)],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == str(expected_count), f"Неверное количество {pattern} записей"

# Тест 4: Проверка прав доступа к файлам
def test_file_permissions(tmp_path):
    """Проверка изменения прав доступа"""
    test_file = tmp_path / "secure.txt"
    test_file.touch()

    # Меняем права доступа
    subprocess.run(['chmod', '600', str(test_file)])

    # Получаем текущие права
    st_mode = os.stat(test_file).st_mode
    assert oct(st_mode)[-3:] == '600', "Права доступа должны быть 600"

# Тест 5: Проверка системной информации
def test_system_info():
    """Проверка базовой информации о системе"""
    # Проверяем версию ядра
    uname_result = subprocess.check_output(['uname', '-r'])
    assert len(uname_result) > 0, "Информация о ядре должна быть доступна"

    # Проверяем использование диска
    df_result = subprocess.run(['df', '-h'], capture_output=True, text=True)
    assert "/dev/" in df_result.stdout, "Информация о дисках должна быть доступна"

# Тест 6: Демонстрация работы с bash-скриптами
def test_bash_script_execution(tmp_path):
    """Создание и выполнение простого bash-скрипта"""
    script = tmp_path / "demo_script.sh"
    script_content = """#!/bin/bash
echo "Script executed successfully"
exit 0
"""
    script.write_text(script_content)

    # Даем права на выполнение
    os.chmod(script, 0o755)

    # Запускаем скрипт
    result = subprocess.run(
        [str(script)],
        capture_output=True,
        text=True
    )

    assert "successfully" in result.stdout
    assert result.returncode == 0