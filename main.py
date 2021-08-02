import os

from dhooks import Webhook, Embed

from sites.course_scorpion import CourseScorpion
from models.course import Course


WEBHOOK_URL = os.environ['udemy_discord_webhook']

course_scorpion = CourseScorpion(pages_to_scrape=2)


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


# TODO Parse the Udemy URL and remove any 'ad' or 'campaign' references
# TODO Add the courses to a DB so that they don't get posted multiple times
# TODO Add other sites

url = 'https://couponscorpion.com/business/istqb-foundation-level-ctfl-training-for-2021-1000-quiz/'
course = Course(
    title = course_scorpion.get_course_title(url),
    description = course_scorpion.get_course_description(url),
    image_url = course_scorpion.get_course_image(url),
    store_url = course_scorpion.get_udemy_link(url)
)
#courses = course_scorpion.find_courses()
createDiscordEmbed(course)
