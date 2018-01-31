# --*-- coding: utf-8 --*--
from flask import request


def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page', 10)
    search_msg = request.args.get('search_msg')
    if not per_page:
        per_page = 10
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset, search_msg
