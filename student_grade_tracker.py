# 📚 Advanced Student Grade Tracker (OOP Version)

import csv
import matplotlib.pyplot as plt
import random

# ------------------- Student Class -------------------
class Student:
    def __init__(self, name):
        self.name = name
        self.subjects = {}

    def add_subject(self, subject):
        if subject not in self.subjects:
            self.subjects[subject] = []

    def add_grade(self, subject, grade):
        self.add_subject(subject)
        self.subjects[subject].append(grade)

    def delete_subject(self, subject):
        if subject in self.subjects:
            del self.subjects[subject]

    def delete_grade(self, subject, index):
        if subject in self.subjects and 0 <= index < len(self.subjects[subject]):
            return self.subjects[subject].pop(index)
        return None

    def get_average(self):
        all_grades = [grade for grades in self.subjects.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def get_subject_average(self, subject):
        grades = self.subjects.get(subject, [])
        return sum(grades) / len(grades) if grades else 0

    def report(self):
        lines = [f"Student: {self.name}"]
        for subject, grades in self.subjects.items():
            avg = self.get_subject_average(subject)
            lines.append(f"{subject}: {grades} | Avg: {avg:.2f}")
        lines.append(f"Overall Average: {self.get_average():.2f}%")
        return "\n".join(lines)

    def __repr__(self):
        return self.report()
# ------------------- Academy Class -------------------
class Academy:
    def __init__(self):
        self.students = {}

    def get_student(self, name):
        return self.students.get(name)

    def add_student(self, name):
        if name not in self.students:
            self.students[name] = Student(name)

    def delete_student(self, name):
        if name in self.students:
            del self.students[name]

    def get_top_student(self):
        top = max(self.students.values(), key=lambda s: s.get_average(), default=None)
        if top:
            print(f"\n🏆 Top Student: {top.name} with Avg: {top.get_average():.2f}%")
        else:
            print("No students found.")

    def get_subject_average(self, subject):
        grades = []
        for student in self.students.values():
            grades.extend(student.subjects.get(subject, []))
        if grades:
            print(f"Average for {subject}: {sum(grades) / len(grades):.2f}%")
        else:
            print(f"No data for {subject}.")

    def save_to_csv(self):
        with open("students_report.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Subject", "Grade"])
            for student in self.students.values():
                for subject, grades in student.subjects.items():
                    for grade in grades:
                        writer.writerow([student.name, subject, grade])
        print("Data saved to students_report.csv")

    def export_individual_report(self, name):
        student = self.get_student(name)
        if student:
            filename = f"{student.name.replace(' ', '_')}_report.txt"
            with open(filename, 'w') as f:
                f.write(student.report())
            print(f"Saved report to {filename}")
        else:
            print("Student not found.")

    def plot_student_grades(self, name):
        student = self.get_student(name)
        if not student:
            print("Student not found.")
            return
        subjects = list(student.subjects.keys())
        avgs = [student.get_subject_average(subj) for subj in subjects]
        plt.bar(subjects, avgs)
        plt.title(f"Average Grades for {student.name}")
        plt.ylabel("Average")
        plt.show()

    def generate_dummy_data(self, n):
        sample_subjects = ["Math", "Science", "English", "Art"]
        for i in range(n):
            name = f"Student{i+1}"
            self.add_student(name)
            for subj in sample_subjects:
                for _ in range(3):
                    grade = random.randint(50, 100)
                    self.students[name].add_grade(subj, grade)
        print(f"Generated {n} dummy students.")

    def debug_print_structure(self):
        from pprint import pprint
        pprint(self.students)

# ------------------- Main Menu -------------------
def main():
    academy = Academy()

    while True:
        print("\n--- Student Grade Tracker Menu ---")
        print("1. Add Student")
        print("2. Add Subject")
        print("3. Add Grade")
        print("4. Delete Student")
        print("5. Delete Subject")
        print("6. Delete Grade")
        print("7. Show Top Student")
        print("8. Show Subject Average")
        print("9. Plot Student Grades")
        print("10. Export Individual Report")
        print("11. Save All to CSV")
        print("12. Generate Dummy Data")
        print("13. Debug Print")
        print("14. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter student name: ").strip().title()
            academy.add_student(name)

        elif choice == '2':
            name = input("Enter student name: ").strip().title()
            student = academy.get_student(name)
            if student:
                subject = input("Enter subject: ").strip().title()
                student.add_subject(subject)

        elif choice == '3':
            name = input("Enter student name: ").strip().title()
            student = academy.get_student(name)
            if student:
                subject = input("Enter subject: ").strip().title()
                try:
                    grade = float(input("Enter grade (0-100): "))
                    student.add_grade(subject, grade)
                except ValueError:
                    print("Invalid grade.")

        elif choice == '4':
            name = input("Enter student name to delete: ").strip().title()
            academy.delete_student(name)

        elif choice == '5':
            name = input("Enter student name: ").strip().title()
            student = academy.get_student(name)
            if student:
                subject = input("Enter subject to delete: ").strip().title()
                student.delete_subject(subject)

        elif choice == '6':
            name = input("Enter student name: ").strip().title()
            student = academy.get_student(name)
            if student:
                subject = input("Enter subject: ").strip().title()
                try:
                    index = int(input("Enter index of grade to delete: "))
                    deleted = student.delete_grade(subject, index)
                    print(f"Deleted: {deleted}")
                except ValueError:
                    print("Invalid index.")

        elif choice == '7':
            academy.get_top_student()

        elif choice == '8':
            subject = input("Enter subject: ").strip().title()
            academy.get_subject_average(subject)

        elif choice == '9':
            name = input("Enter student name: ").strip().title()
            academy.plot_student_grades(name)

        elif choice == '10':
            name = input("Enter student name: ").strip().title()
            academy.export_individual_report(name)

        elif choice == '11':
            academy.save_to_csv()

        elif choice == '12':
            academy.generate_dummy_data(5)

        elif choice == '13':
            academy.debug_print_structure()

        elif choice == '14':
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
