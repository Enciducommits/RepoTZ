#!/bin/bash

# Получаем список юнитов, начинающихся на "foobar-"
units=$(systemctl list-units --type=service --all | grep 'foobar-' | awk '{print $1}')

# Проходим по каждому юниту
for unit in $units; do
    echo "Обработка юнита: $unit"

    # Остановка юнита
    systemctl stop "$unit"

    # Получаем рабочую директорию и имя сервиса
    working_dir=$(systemctl show "$unit" -p WorkingDirectory | cut -d'=' -f2)
    service_name=$(basename "$working_dir")

    # Перемещение файлов в новую директорию
    new_dir="/srv/data/$service_name"
    mkdir -p "$new_dir"
    mv "$working_dir/"* "$new_dir/"

    # Обновление параметров в файле юнита
    unit_file="/etc/systemd/system/$unit"
    sed -i "s|^WorkingDirectory=.*|WorkingDirectory=$new_dir|g" "$unit_file"
    sed -i "s|^ExecStart=.*|ExecStart=$new_dir/foobar-daemon произвольные_параметры|g" "$unit_file"

    # Перезагрузка конфигурации systemd
    systemctl daemon-reload

    # Запуск юнита
    systemctl start "$unit"

    echo "Юнит $unit успешно обработан."
done

echo "Все юниты обработаны."
