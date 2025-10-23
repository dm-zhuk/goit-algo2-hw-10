import json


# Визначення класу Teacher
class Teacher:
    def __init__(self, first_name, last_name, age, email, by_subject):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.by_subject = by_subject
        self.assigned_subjects = set()


def create_schedule(subjects, teachers):
    """
    Призначає викладачів на предмети, використовуючи жадібний алгоритм.
    """
    uncovered = subjects.copy()
    selected_teachers = []
    while uncovered:
        best_teacher = None
        best_cover_count = -1
        best_age = float("inf")

        for teacher in teachers:
            cover = teacher.by_subject & uncovered
            count = len(cover)
            if count > best_cover_count or (
                count == best_cover_count and teacher.age < best_age
            ):
                best_teacher = teacher
                best_cover_count = count
                best_age = teacher.age

        if best_teacher is None or best_cover_count == 0:
            return None  # Неможливо покрити

        # Призначити предмети цьому викладачу
        assigned = best_teacher.by_subject & uncovered
        best_teacher.assigned_subjects = assigned
        uncovered -= assigned
        selected_teachers.append(best_teacher)

    return selected_teachers


if __name__ == "__main__":
    # Отримуємо множину предметів з JSON
    with open("subjects.json", "r", encoding="utf-8") as f:
        subjects_list = json.load(f)
    subjects = set(subjects_list)
    # Отримуємо дані про викладачів з JSON
    with open("teachers.json", "r", encoding="utf-8") as f:
        teachers_data = json.load(f)
    # Створюємо список об'єктів класу Teacher на основі даних
    teachers = []
    for data in teachers_data:
        can_teach = set(data["by_subject"])
        teachers.append(
            Teacher(
                data["first_name"],
                data["last_name"],
                data["age"],
                data["email"],
                can_teach,
            )
        )

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(
                f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}"
            )
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")

"""
Розклад занять:
Наталія Шевченко, 29 років, email: n.shevchenko@example.com
   Викладає предмети: Біологія, Хімія\n
Дмитро Бондаренко, 35 років, email: d.bondarenko@example.com
   Викладає предмети: Інформатика, Фізика\n
Олександр Іваненко, 45 років, email: o.ivanenko@example.com
   Викладає предмети: Математика\n

Щоб мінімізувати кількість викладачів і все одно покрити всі предмети, можна звільнити наступних:\n
Марія Петренко, Сергій Коваленко та Олена Гриценко.\n
Решта (Шевченко, Бондаренко та Іваненко) достатньо для розкладу.
"""
