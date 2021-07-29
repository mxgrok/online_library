import json
import os
import sys

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_books_info(books_file_path: str):
    if not (os.path.exists(books_file_path)):
        return

    with open(books_file_path, 'r') as books_file:
        books_file = books_file.read()
        return json.loads(books_file)


def render_pagination(templates_path: str, template: str, destination_path: str, book_info: list):
    env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template)
    pagination = template.render(book_info=book_info)

    with open(f'{destination_path}/index.html', 'w', encoding='utf-8') as file:
        file.write(pagination)


def run_server(templates_path, pagination_template, rendered_files_path, book_info):
    render_pagination(templates_path, pagination_template, rendered_files_path, book_info)
    server = Server()
    server.watch('templates/*.html', render_pagination(templates_path, pagination_template, rendered_files_path, book_info))
    server.serve(root=rendered_files_path)


if __name__ == '__main__':
    root_path = os.path.abspath(os.path.dirname(__file__))
    books_storage_root_path = os.path.join(root_path, 'books_storage')
    books_path = os.path.join(books_storage_root_path, 'books')
    images_path = os.path.join(books_storage_root_path, 'images')

    rendered_files_path = os.path.join(root_path, 'html_rendered')
    os.makedirs(rendered_files_path, exist_ok=True)

    templates_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
    pagination_template = 'pagination_template.html'

    book_info_json = os.path.join(books_storage_root_path, 'book_info.json')
    book_info = get_books_info(book_info_json)

    if not book_info:
        sys.exit(1)

    run_server(templates_path, pagination_template, rendered_files_path, book_info)
