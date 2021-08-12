from bs4 import BeautifulSoup as bs
from login import AO3_URL, login
from datetime import date
import json
from config import CRED_PATH

# TODO diff/merge support
# TODO add beg notes and end notes support
# TODO title in metadata support
# TODO init
# TODO get author token


def get_list_works():
    session = login(CRED_PATH)
    works_html = session.get(AO3_URL + 'users/Ellana42/works').text
    works_page = bs(works_html, 'html.parser')
    works_links = works_page.find('ol', {
        'class': 'work index group'
    }).findAll('li', recursive=False)
    works = {
        work.find('a').text: work.find('a')['href']
        for work in works_links
    }
    return works


def get_work(title):
    session = login(CRED_PATH)
    works = get_list_works()
    if title not in works.keys():
        print('This title is invalid')
        return None
    work = session.get(AO3_URL + works[title]).text
    return bs(work, 'html.parser')


def get_chapters(work):
    chap_list = work.find('div', {
        'id': 'workskin'
    }).findAll(
        lambda tag: tag.name == 'div' and tag.get('class') == ['chapter'])
    chapters = [get_chap_text(chapter) for chapter in chap_list]
    chapters_metadata = {
        i + 1: {
            'summary': get_summary(chapter),
            'url': get_chap_url(chapter)
        }
        for i, chapter in enumerate(chap_list)
    }
    return chapters, chapters_metadata


def get_chap_text(chapter):
    text = '\n'.join([
        par.text for par in chapter.find('div', {
            'class': 'userstuff module',
            'role': 'article'
        }).findAll('p')
    ])
    return text


def get_summary(chapter):
    summary_module = chapter.find('div', {'class': 'summary module'})
    if summary_module:
        return summary_module.find('p').text
    else:
        return ''


def get_chap_url(chapter):
    link = chapter.find('li').a['href']
    return link


def load_work_metadata():
    with open('metadata.json') as metadata_file:
        metadata = json.load(metadata_file)
    return metadata


def load_chapter_metadata(chapter_nb):
    metadata = load_work_metadata()
    return metadata[str(chapter_nb)]


def load_text(chapter_nb):
    with open('chapter_{}.md'.format(str(chapter_nb)), 'r') as chap_file:
        text = chap_file.read()
    return text


def post_chapter(chapter_nb):
    session = login(CRED_PATH)
    chapter_day, chapter_month, chapter_year = date.today().day, date.today(
    ).month, date.today().year
    metadata = load_chapter_metadata(chapter_nb)
    chapter_content = load_text(chapter_nb)
    chapter_sum, chapter_url = metadata['summary'], metadata['url']

    edit_page = session.get(AO3_URL + chapter_url)
    auth_token = bs(edit_page.text,
                    'html.parser').find('meta',
                                        {'name': 'csrf-token'})['content']
    form_data = {
        'utf8': '✓',
        '_method': 'patch',
        'authenticity_token': auth_token,
        'chapter[title]': '',
        'chapter[position]': chapter_nb,
        'chapter[wip_length]': chapter_nb,
        'chapter[published_at(3i)]': chapter_day,
        'chapter[published_at(2i)]': chapter_month,
        'chapter[published_at(1i)]': chapter_year,
        'chapter[author_attributes][ids][]': '8812570',
        'chapter[author_attributes][byline]': '',
        'chapter[summary]': chapter_sum,
        'front-notes-options-show': '1',
        'chapter[notes]': '',
        'end-notes-options-show': '1',
        'chapter[endnotes]': '',
        'chapter[content]': chapter_content,
        'post_without_preview_button': 'Post'
    }

    return session.post(
        AO3_URL + chapter_url[:-5],
        data=form_data,
    )


def pull(title):
    work = get_work(title)
    chapters, metadata = get_chapters(work)
    for i, chapter in enumerate(chapters):
        with open('chapter_{}.md'.format(i + 1), 'w') as file:
            file.write(chapter)
    with open('metadata.json', 'w') as summary_file:
        json.dump(metadata, summary_file)


def push():
    work_metadata = load_work_metadata() 
    for chapter in work_metadata:
        post_chapter(chapter)


def init_work():
    pass
