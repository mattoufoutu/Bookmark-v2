from flask import Blueprint, request

from bookmark import app
from bookmark.settings import VERSION
from bookmark.service import get_tagcloud, get_tag, get_list_bookmark


from .item.Bookmark import ItemBookmark
from .item.Tag import ItemTag

import json

b = Blueprint('api', __name__)

SEPARATOR = '+'


@b.route('/', methods=['GET', ])
def index():
    return VERSION


@b.route('/bookmarks', methods=['GET', ])
@b.route('/bookmarks/<string:tags>', methods=['GET', ])
def bookmarks(tags=None):
    filters = []
    if tags is not None:
        filters = [x.id for x in
            [get_tag(x) for x in tags.split(SEPARATOR)]
            if x is not None]

    bookmarks = get_list_bookmark(filters)
    bookmark_list = []

    for b in bookmarks:
        bookmark = ItemBookmark(b.id, b.tags, b.link, b.title, b.description)
        bookmark_list.append(bookmark)

    bookmark_list = map(lambda x: x.json(), bookmark_list)
    response = app.make_response(json.dumps(bookmark_list))
    response.mimetype = 'application/json'
    return response


@b.route('/tagcloud', methods=['GET', ])
@b.route('/tagcloud/<string:tags>', methods=['GET', ])
def tagcloud(tags=None):
    filters = []
    if tags is not None:
        filters = [get_tag(x).id for x in tags.split(SEPARATOR)]

    tagcloud = get_tagcloud(filters)
    tag_list = []
    for (t, count) in tagcloud:
        tag = ItemTag(t.id, t.name, count)
        tag_list.append(tag)
    tags_list = map(lambda x: x.json(),
        tag_list)
    response = app.make_response(json.dumps(tags_list))
    response.mimetype = 'application/json'
    return response