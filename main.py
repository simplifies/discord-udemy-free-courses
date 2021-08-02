import os

from dhooks import Webhook, Embed
import sqlalchemy as db
from database.courses import CoursesTable

from sites.course_scorpion import CourseScorpion
from sites.udemy_coupons_me import UdemyCoupons
from models.course import Course
from database.courses import CoursesTable


WEBHOOK_URL = os.environ['udemy_discord_webhook']

# setup DB
db_connection = CoursesTable()

# get course classes
#course_scorpion = CourseScorpion(pages_to_scrape=2)
udemy_coupons_me = UdemyCoupons(num_of_courses=20)


def createDiscordEmbed(course: Course):
    hook = Webhook(WEBHOOK_URL)
    course_embed = Embed(
        title=course.title,
        description=course.description,
        url=course.store_link,
        image_url=course.image_url,
        color=0x5CDBF0,
        timestamp='now'  # sets the timestamp to current time
    )

    hook.send(embed=course_embed)


udemy_coupons_me_courses = udemy_coupons_me.find_courses()


for course in udemy_coupons_me_courses:
    if not db_connection.is_already_in_db(course.title):
        db_connection.insert_course(course)
        createDiscordEmbed(course)
    else:
        print(f"[-] {course.title} is already in the DB. Skipping...")
