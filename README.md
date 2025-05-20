# 🛠️ Free XLS FileService

**Free XLS FileService** — это бесплатный кроссплатформенный веб-сервис для некоммерческого использования, который позволяет работать с данными из Excel-файлов как с SQL-таблицами. С его помощью можно обращаться к данным Excel через web API, отправляя GET-запросы, например, из макросов Р7-Офис.


## Установка и запуск сервиса

### Вариант 1: Ручной запуск из исходников

```bash
git clone https://github.com/r7-consult/r7_fileservice.git
cd r7_fileservice
pip install -r requirements.txt
python -m xldb-proxy-file
```

### Вариант 2: Запуск из готовой сборки

Скачайте исполняемый файл для вашей системы:

- [⬇ Windows](./build/r7_fileservice-windows.exe)
- [⬇ Ubuntu](./build/r7_fileservice-ubuntu.bin)
- [⬇ RedOS](./build/r7_fileservice-redos.bin)
- [⬇ AstraOS](./build/r7_fileservice-astra.bin)

Затем просто выполните:

```bash
./r7_fileservice-[os] //запустите нужный билд
``` 
По умолчанию сервис запускается на http://127.0.0.1:58081

## Возможности и примеры работы

### GET /file/list
Получение списка файлов в директории
```bash
http://localhost:58081/file/list?path=C:\
```
Ответ:
- Успех: `{"files": ["file1.xlsx", "file2.xlsx", ...]}` - список файлов
- Ошибка: HTTP 500 с описанием ошибки (например, директория не существует)

### GET /file/available
Проверка существования файла
```bash
http://localhost:58081/file/available?path=C:\&file_name=example.xlsx
```
Ответ:
- Файл существует: `{"status": "OK"}`
- Файл не существует: `{"status": "Error"}`
- Ошибка: HTTP 500 с описанием ошибки

### GET /file/meta
Получение метаданных файла
```bash
http://localhost:58081/file/meta?path=C:\&file_name=example.xlsx
```
Ответ:
- Успех: JSON с метаданными файла:
  ```json
  {
    "file_name": "example.xlsx",
    "file_path": "C:\\example.xlsx",
    "size_bytes": 1234,
    "created_at": "2025-05-20T12:00:00",
    "modified_at": "2025-05-20T12:00:00",
    "accessed_at": "2025-05-20T12:00:00",
    "mode": "0o100666",
    "sheets": ["Sheet1", "Sheet2"],
    "copyright": "Free for non commercial use https://r7-consult.ru/"
  }
  ```
- Ошибка: HTTP 500 с описанием ошибки

### GET /file/register
Проверка возможности чтения Excel-файла и получение информации о его структуре
```bash
http://localhost:58081/file/register?path=C:\&file_name=example.xlsx&sheet_name=Sheet1&usecols=A,B,C&skiprows=0&nrows=1000
```
Параметры:
- `sheet_name`: имя листа (опционально)
- `usecols`: список колонок (опционально)
- `skiprows`: пропустить строк сверху (по умолчанию 0)
- `nrows`: максимальное число строк (по умолчанию 10000000)

Ответ:
- Успех: `{"columns": ["col1", "col2", ...], "rows": 1000}` - список колонок и количество строк в файле
- Ошибка: HTTP 500 с описанием ошибки

### GET /file/sql
Выполнение SQL-запроса к Excel-файлу
```bash
http://localhost:58081/file/sql?query=select%20*%20from%20df&path=C:\&file_name=example.xlsx&sheet_name=Sheet1
```
Параметры:
- Те же, что и для `/file/register`
- `query`: SQL-запрос (данные доступны в таблице с именем `df`)

Примеры запросов:
```sql
select * from df                           -- все данные
select col1, col2 from df                  -- только нужные колонки
select * from df where col1 > 100          -- с условием
select col1, count(*) from df group by col1 -- с группировкой
```

Ответ:
- Успех: Массив записей с результатами запроса
- Ошибка: HTTP 500 с описанием ошибки

### Отображение результатов на листе Р7 через макросы

Для отображения результатов SQL-запроса на листе Р7-Офис можно использовать следующий макрос:

```javascript
(function() {
  // URL с SQL-запросом к файлу Excel
  var url = "http://localhost:58081/file/sql?query=select%20*%20from%20df&path=C:\\tt&file_name=address.xlsx&sheet_name=Sheet1";

  fetch(url)
    .then(response => response.json())  // Парсим ответ как JSON
    .then(data => {
      var oWorksheet = Api.GetActiveSheet();  // Получаем активный лист

      // Считываем заголовки из первого объекта JSON
      var headers = Object.keys(data[0]);

      // Преобразуем данные в двумерный массив по порядку заголовков
      var sData = data.map(row => headers.map(h => row[h] || ''));

      // Объединяем заголовки и строки данных
      var fullArray = [headers, ...sData];

      // Получаем диапазон для всей таблицы
      var dataRange = oWorksheet.GetRange(
        oWorksheet.GetRangeByNumber(0, 0),
        oWorksheet.GetRangeByNumber(fullArray.length - 1, headers.length - 1)
      );

      // Вставляем все значения одной операцией
      dataRange.SetValue(fullArray);

      // Перерисовываем документ
      Api.asc_calculate(Asc.c_oAscCalculateType.ActiveSheet);
    })
    .catch(error => {
      console.log("Ошибка при получении данных:", error);
    });
})();
```

Макрос выполняет следующие действия:
1. Отправляет GET-запрос к сервису с SQL-запросом
2. Получает данные в формате JSON
3. Преобразует данные для вставки в таблицу:
   - Первая строка - заголовки колонок
   - Остальные строки - данные из результата запроса
4. Вставляет данные в активный лист, начиная с ячейки A1
5. Обновляет отображение листа

> **Важно**: Для отображения изменений после выполнения макроса используется команда `Api.asc_calculate()`, так как по умолчанию макрос не обновляет содержимое документа.

## Структура проекта

```text
r7_fileservice/
├── src/
│   ├── logger_conf.py
│   ├── main.py
│   ├── r7_fileservice.py
│   ├── reporting.py
│   ├── svc_xls_files.py
│   └── types_meta.py
├── build/
│   ├── r7_fileservice-windows.exe
│   ├── r7_fileservice-ubuntu.bin
│   ├── r7_fileservice-redos.bin
│   └── r7_fileservice-astra.bin
├── requirements.txt
└── README.md
```


## Контакты
- Сайт: [Р7-Консалт](https://r7-consult.ru/)
- Email: er@exceldb.pro
- Телефон: +7 915 258-0371
- Telegram: https://t.me/r7_js
