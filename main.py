import sqlite3
from pathlib import Path

folder = Path(__file__).resolve().parent
con = sqlite3.connect(folder / "app.db")

# ============ 1. Создание таблицы ============
con.execute("""
CREATE TABLE IF NOT EXISTS stands (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    value INTEGER
)
""")

# ============ 2. Исходные данные (8 записей, 3 категории) ============
data = [
    ("Яндекс", "Технологии", 60),
    ("Сбер", "Технологии", 95),
    ("VK", "Технологии", 75),
    ("МТС", "Технологии", 120),
    ("Третьяковка", "Искусство", 70),
    ("Эрмитаж", "Искусство", 110),
    ("ВкусВилл", "Еда", 50),
    ("Перекресток", "Еда", 85),
]

count = con.execute("SELECT COUNT(*) FROM stands").fetchone()[0]
if count == 0:
    con.executemany(
        "INSERT INTO stands (name, category, value) VALUES (?, ?, ?)",
        data,
    )
    con.commit()

# ============ 3. Все записи ============
print("Все записи:")
for row in con.execute("SELECT * FROM stands ORDER BY id"):
    print(row)

# ============ 4. Фильтр по категории ============
chosen_category = "Технологии"
print(f"\nКатегория: {chosen_category}")
for row in con.execute(
    "SELECT * FROM stands WHERE category = ?", (chosen_category,)
):
    print(row)

# ============ 5. Числовой фильтр: value > 80 ============
limit = 80
print(f"\nФильтр: value > {limit}")
for row in con.execute("SELECT * FROM stands WHERE value > ?", (limit,)):
    print(row)

# ============ 6. Сортировка по value ASC ============
print("\nСортировка по value ASC:")
for row in con.execute("SELECT * FROM stands ORDER BY value ASC, id ASC"):
    print(row)

# ============ 7. UPDATE (изменяем ширину стенда id=1) ============
record_id = 1
new_value = 90
con.execute(
    "UPDATE stands SET value = ? WHERE id = ?",
    (new_value, record_id),
)
con.commit()
print(f"\nПосле изменения id={record_id} (ширина = {new_value} см):")
print(con.execute("SELECT * FROM stands WHERE id = ?", (record_id,)).fetchone())

# ============ 8. DELETE (удаляем стенд id=8) ============
record_id = 8
con.execute("DELETE FROM stands WHERE id = ?", (record_id,))
con.commit()
print("\nПосле удаления id=8:")
for row in con.execute("SELECT * FROM stands ORDER BY id"):
    print(row)

con.close()