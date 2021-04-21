from fastapi.encoders import jsonable_encoder


async def generate_next_or_prev_url(count, current_page, page_size, url):
    _prev, _next = None, None
    if current_page == 1 and 'page=1' not in url:
        url += '&page=1'
    if current_page > 1:
        prev_page = f'page={current_page - 1}'
        _prev = url.replace(f'page={current_page}', prev_page)
    if count > current_page * page_size:
        if current_page > 1 and _prev:
            next_page = f'page={current_page + 1}'
            _next = url.replace(f'page={current_page}', next_page)
        else:
            next_page = 'page=2'
            _next = url.replace(f'page={current_page}', next_page)

    return {
        'count': count,
        'next': _next,
        'previous': _prev,
    }


async def paginate(query, page, page_size):
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    return query


async def get_results(query, schema):
    results = []
    for obj in query.all():
        results.append(schema(**jsonable_encoder(obj)))
    return results