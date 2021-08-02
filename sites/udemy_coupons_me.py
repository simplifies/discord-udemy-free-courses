from typing import List
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from models.course import Course


class UdemyCoupons:
    def __init__(self, num_of_courses = 10) -> None:
        self.num_of_courses = num_of_courses  # The maximum number of courses to return
        self.course_pages = []  # List of the individual course pages on udemycourses.me
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'}

        page = requests.get('https://udemycoupons.me', headers=self.headers)
        soup = BeautifulSoup(page.content, "html.parser")
        course_urls = soup.find_all("div", class_="td-module-thumb")

        for course in course_urls:
            page_link = course.findChild("a")
            self.course_pages.append(page_link.get("href"))


    def get_course_title(self, course_page_html: bytes) -> str:
        soup = BeautifulSoup(course_page_html, "html.parser")
        course_title = soup.find("h1", class_="tdb-title-text")

        return course_title.text


    def get_course_description(self, course_page_html: bytes) -> str:
        soup = BeautifulSoup(course_page_html, "html.parser")
        description_div = soup.find("div", attrs={'data-purpose': 'safely-set-inner-html:description:description'})
        try:
            description = description_div.findChild("p")
            return description.text
        except AttributeError:
            return "No description"


    def get_udemy_link(self, course_page_html: bytes) -> str:
        soup = BeautifulSoup(course_page_html, "html.parser")
        udemy_button_span = soup.find("span", class_="td_text_highlight_marker_green")
        udemy_url: str = udemy_button_span.findChild("a").get("href")

        # remove the affiliate and other junk from the Udemy URL, but keep the couponCode parameter
        try:
            parsed_url = urlparse(udemy_url)
            coupon_code = parse_qs(parsed_url.query)['couponCode']
            clean_udemy_url = f'https://{parsed_url.netloc}{parsed_url.path}?couponCode={coupon_code[0]}'
            return clean_udemy_url
        except KeyError:
            return udemy_url


    def get_course_image(self, course_page_html: bytes) -> str:
        soup = BeautifulSoup(course_page_html, "html.parser")
        img_tag = soup.find("img", class_="entry-thumb")
        thumbnail: str = img_tag["data-src"]

        return thumbnail or "https://via.placeholder.com/150"


    def find_courses(self) -> List[Course]:
            courses: List[Course] = []

            for url in self.course_pages:
                course_page_html = requests.get(url, headers=self.headers)
                course_title = self.get_course_title(course_page_html.content)
                course_description = self.get_course_description(course_page_html.content)
                course_url = self.get_udemy_link(course_page_html.content)
                course_image = self.get_course_image(course_page_html.content)

                # limit the list to 'self.num_of_courses' items
                if len(courses) >= self.num_of_courses:
                    return courses
                else:
                    courses.append(
                        Course(
                            title=course_title,
                            description=course_description,
                            store_url=course_url,
                            image_url=course_image
                        )
                    )
