# Договоренность о наименовании
И так понятно, для чего это надо.

## 1. Пакеты
* Имена пакетов начинаются с маленькой буквы
* Слова разделяются символом нижнего подчеркивания(_)

## 2. Классы
* Имена классов в PascalCase
* Классы исключений дополняются в конце словом Error

## 3. Переменные
* Использовать стиль Си(например, train_model)
* Приватные начинаются с нижнего подчеркивания (_model)

## 4. Методы
* См. пункт 3

## 5. Функции
* См. пункт 4

## Константы
* Змеиный регистр из заглавных букв (GOLDEN_RATIO = 1.61803)

## Особые требования
* Стараться использовать явную типизацию
```python
def split_arr(self, arr: List, train_part: float = 0.7) -> (Dict, Dict):
    arr = np.random.permutation(arr)
    train_size = train_part * len(arr)
    train_json = {}
    val_json = {}
    for i, node in enumerate(arr):
        if i <= train_size:
            train_json[node[0]] = node[1]
        else:
            val_json[node[0]] = node[1]
    return train_json, val_json
```
* Иммпортирование типов
```python
from typing import List, Tuple, Dict
```
## Полезные материалы
* [Python Naming Conventions](https://visualgit.readthedocs.io/en/latest/pages/naming_convention.html) - почти весь материал взят здесь
* [PEP 8](https://www.python.org/dev/peps/pep-0008/) - тут вообще все, что надо
* [PEP 8 на русском](https://pythonworld.ru/osnovy/pep-8-rukovodstvo-po-napisaniyu-koda-na-python.html) - тоже самое, но на русском