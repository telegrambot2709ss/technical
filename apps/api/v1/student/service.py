import re
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

from apps.api.v1.base.db import dictfetchall, dictfetchone
from apps.api.v1.base.sqlpaginator import SqlPaginator


def get_student_list(request):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.PER_PAGE))

        page = page if 0 < page else 1
        per_page = per_page if 0 < per_page else settings.PER_PAGE
    except:
        page = 1
        per_page = settings.PER_PAGE

    search = request.query_params.get("search")
    fullname = request.query_params.get('fullname')
    email = request.query_params.get('email')
    username = request.query_params.get('username')
    status = request.query_params.get('status')
    university = request.query_params.get('university')
    contract = request.query_params.get('contract')

    sql = ""
    if not search:
        if fullname or email or username or status or university or contract:
            sql = "where "

        if fullname:
            sql += f"uu.fullname = '{fullname}' and "
        if email:
            sql += f"uu.email = '{email}' and "
        if username:
            sql += f"uu.username = '{username}' and "
        if status:
            sql += f"us.status = '{status}' and "
        if university:
            sql += f"us.university ILIKE '%{university}%' and "
        if contract and (type(contract) == int or contract.isdigit()):
            sql += f"us.contract = {int(contract)} and "

        sql = sql.strip("and ")
    elif search:
        sql += f"Where uu.fullname ILIKE '%{search}%' or uu.email ILIKE '%{search}%' or uu.username ILIKE '%{search}%' or us.university ILIKE '%{search}%'"

    student_count = _query_student_count(sql=sql)
    students = _query_student_list(sql=sql, page=page, per_page=per_page)

    items = []
    for student in students:
        items.append(OrderedDict([
            ("id", student['id']),
            ("fullname", student['fullname']),
            ("email", student['email']),
            ("username", student['username']),
            ("status", student['status']),
            ("university", student['university']),
            ("contract", price_format(student['contract'])),
            ("date_joined", student['date_joined'].strftime("%Y-%m-%d %H:%M:%S"))
        ]))

    paginator = SqlPaginator(request, page=page, per_page=per_page, count=student_count)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_student_list(sql, page, per_page):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(f""" 
            select us.*, uu.fullname , uu.username , uu.email , uu.date_joined 
            from users_student us 
            inner join users_user uu ON uu.id = us.user_id 
            {sql}
            LIMIT {per_page} OFFSET {offset}
        """)
        rows = dictfetchall(cursor)

    return rows


def _query_student_count(sql):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""
            select count(1) as cnt
            from users_student us 
            inner join users_user uu on uu.id = us.user_id 
            {sql}
        """)
        row = dictfetchone(cursor)

    result = row['cnt'] if row else 0
    return result


def price_format(inp):
    try:
        price = int(inp)
        res = "{:,}".format(price)
        price = re.sub(",", " ", res)
        return price
    except:
        return inp
