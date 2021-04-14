from bs4 import BeautifulSoup as bs
from login import AO3_URL, login
import re

cred_file = '/Users/Mathilde/Documents/resources/utilities/creds/ao3-creds.json'

def get_list_works(session):
    session = login(cred_file)
    works_html = session.get(AO3_URL + 'users/Ellana42/works').text
    works_page = bs(works_html, 'html.parser')
    works_links = works_page.find('ol', {'class' : 'work index group'}).findAll('li', recursive=False)
    works = {work.find('a').text : work.find('a')['href'] for work in works_links}
    return works

def get_work(title, session):
    works = get_list_works(session)
    if title not in works.keys():
        print('This title is invalid')
        return None
    work = session.get(AO3_URL + works[title]).text
    return bs(work, 'html.parser')

def get_chapters(work):
    chap_list = work.find('div', {'id': 'workskin'}).findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['chapter'])
    chapters = [get_chap_text(chapter) for chapter in chap_list]
    chapters_metadata = []
    return chapters

def get_chap_text(chapter):
    text = '\n'.join([par.text for par in chapter.find('div', {'class': 'userstuff module', 'role' : 'article'}).findAll('p')])
    return text

def post_chapter():
    form_data = {
        'chapter[position]': chapter_nb,
        'chapter[published_at(3i)]' : chapter_day,
        'chapter[published_at(2i)]' : chapter_month,
        'chapter[published_at(1i)]' : chapter_year,
        'chapter[author_attributes][ids][]': 8812570,
        'chapter[summary]': chapter_sum,
        'chapter[content]' : chapter_content,
        'authenticity_token': auth_token,
    }

    session.post(
        chapter_url,
        data=form_data,
    )


def pull(title, session):
    session = login(cred_file)
    work = get_work(title, session)
    chapters = get_chapters(work)
    for i, chapter in enumerate(chapters):
        with open('chapter_{}.md'.format(i + 1), 'w') as file:
            file.write(chapter)


def push(title, file, chapter_number=None):
    session = login(cred_file)
    if not chapter_number:
        chapter_number = re.search('\d*', file).string


