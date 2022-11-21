# Игра Game Lands

Игровой процесс, в котором игрок сможет выбрать персонажа и землю, с которой начнется развитие территорий.
Первый этап начинается с первой выбранной земли, происходит развитие, построение экономики. Каждая земля ограничена количеством возможных построек в зависимости от её размеров.
Каждая постройка даёт определенное количество ресурсов. Добытые ресурсы можно продавать, покупать необходимое – строить крепость, развивать армию. 
В процессе развития земли можно присоединить следующую землю. Для присоединения происходит оценка ресурсов – армия в крепости и армия атакующая.
Игра имеет вид браузерной игры. 

# Сервисы:
- сервис управления землями;
- сервис управления постройками;
- сервис управления ресурсами;
- сервис сбора ресурсов;
- сервис управления боями;
- сервис рынка;
- пользовательский сервис;
- сервис проверки полномочий;
- сервис управления конфигурацией игрового процесса.

# Сервис управления землями: 
- добавляет землю игроку; 
- возвращает список земель; 
- возвращает информацию о земле; 
- обновляет информацию о земле; 
- удаляет землю из базы.

# Запуск сервиса управления землями
uvicorn app:app --port 5000 --reload (запуск из папки land-management)

# Запуск сервиса управления ресурсами
uvicorn app:app --port 5001 --reload (запуск из папки resource-management)

# Запуск сервиса управления постройками
uvicorn app:app --port 5002 --reload (запуск из папки building-management)
