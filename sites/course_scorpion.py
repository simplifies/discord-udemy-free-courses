from typing import List

import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from models.course import Course


class CourseScorpion:
    def __init__(self, pages_to_scrape = 1) -> None:
        self.pages_to_scrape = pages_to_scrape  # how many pages to scrap
        self.course_pages = []  # List of the individual course pages on CourseScorpion.com
        
        for page_number in range(self.pages_to_scrape):
            page_number += 1
            page = requests.get(f'https://couponscorpion.com/category/100-off-coupons/page/{page_number}')
            soup = BeautifulSoup(page.content, "html.parser")

            free_courses = soup.find_all("h2", class_="font120")

            for course in free_courses:
                link = course.find("a")
                self.course_pages.append(link.get("href"))


    def get_course_title(self, course_page_url) -> str:
            page = requests.get(course_page_url)
            soup = BeautifulSoup(page.content, "html.parser")
            course_main_text = soup.find("div", class_="single_top_main")
            title = course_main_text.findChild("h1", recursive=False)
            title = title.text

            return title


    def get_course_description(self, course_page_url) -> str:
        page = requests.get(course_page_url)
        soup = BeautifulSoup(page.content, "html.parser")
        course_main_text = soup.find("div", class_="single_top_main")
        description_div = course_main_text.findChild("div", recursive=False)
        description = description_div.findChild("p")
        description = description.text

        return description
    

    def get_udemy_link(self, course_page_url) -> str:
        # use requests-html to get the 'offer button' URL by waiting for the Javascript to load
        session = HTMLSession()
        resp = session.get(course_page_url)
        resp.html.render(sleep=1, keep_page=True, scrolldown=7)

        # use BeautifulSoup to find the URL of the 'offer button'
        soup = BeautifulSoup(resp.html.html, "html.parser")
        offer_button = soup.find("a", class_="btn_offer_block")
        proxy_url = offer_button.get('href')

        # if we can't get the Udemy URL from the Javascript, then just return the CourseScorpion page URL
        if proxy_url == 'javascript:void(0)':
            return course_page_url
        else:
            # use requests to get the redirected URL for the actual Udemy course
            response = requests.get(proxy_url)
            return response.url


    def get_course_image(self, course_page_url) -> str:
        page = requests.get(course_page_url)
        soup = BeautifulSoup(page.content, "html.parser")
        img_tag = soup.find("div", class_="title_single_area").find("div").find("figure").find("img")
        course_image: str = img_tag["data-ezsrc"]

        return course_image or "https://via.placeholder.com/150"


    def find_courses(self) -> List[Course]:
        courses = []

        for url in self.course_pages:
            course_title = self.get_course_title(url)
            course_description = self.get_course_description(url)
            course_url = self.get_udemy_link(url)
            course_image = self.get_course_image(url)

            courses.append(
                Course(
                    title=course_title,
                    description=course_description,
                    store_url=course_url,
                    image_url=course_image
                )
            )
        
        return courses
