import sqlite3

from models.course import Course


class CoursesTable():
    def __init__(self) -> None:
        self.connection = sqlite3.connect('udemy_courses.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS courses(
                title varchar NOT NULL,
                description varchar NOT NULL,
                image_url varchar NOT NULL,
                store_url varchar NOT NULL);
            """
        )


    def is_already_in_db(self, title: str):
        results = self.cursor.execute(
            "SELECT * FROM courses WHERE title=?",
            (title,)
        )
        results = results.fetchone()

        return results


    def insert_course(self, course: Course):
        self.cursor.execute(
            "INSERT INTO courses(title, description, image_url, store_url) VALUES(?, ?, ?, ?);",
            (course.title, course.description, course.image_url, course.store_link)
        )
        self.connection.commit()


    def close(self):
        self.connection.close()

