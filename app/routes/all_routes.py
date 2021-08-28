import aiohttp_jinja2
from aiohttp import web

from app.database import products as prod_db, kinds as kind_db
from app.middlewares.checks import find_product


async def dashboard(request: web.Request):
    context = {"page": "dashboard"}
    return await aiohttp_jinja2.render_template_async(
        "dashboard.html", request, context
    )


async def products(request: web.Request):
    if await request.post():
        data = await request.post()
        label = data["label"]
        amount = data["amount"]
        kind = data["kind"]
        about = data["about"]
        picture = data["picture"]
        if not await find_product(label):
            await prod_db.add_product(label, amount, kind, about, picture)
            print("Додано")
        else:
            print("Вже є")
    data = request.query
    if not "pages" in data:
        pages = skip = 0
    else:
        pages = int(data["pages"])
        skip = pages * 10
    if not "sort" in data:
        sort = "none"
    else:
        sort = data["sort"]
    page_count = await prod_db.get_count_products(sort)
    products = await prod_db.get_products(10, skip, sort)
    kinds = await kind_db.find_kinds()
    prod_list = []
    kind_list = []
    async for prod in products:
        prod_list.append(prod)
    async for kind in kinds:
        kind_list.append(kind)
    context = {
        "page": "products",
        "products": prod_list,
        "count": page_count,
        "kinds": kind_list,
        "request": request,
        "cur_page": pages+1,
    }
    return await aiohttp_jinja2.render_template_async("products.html", request, context)


async def departments(request: web.Request):
    context = {"page": "departments"}
    return await aiohttp_jinja2.render_template_async(
        "departments.html",
        request, context
    )


async def invoices(request: web.Request):
    context = {"page": "invoices"}
    return await aiohttp_jinja2.render_template_async(
        "invoices.html",
        request, context
    )


async def reports(request: web.Request):
    context = {"page": "reports"}
    return await aiohttp_jinja2.render_template_async(
        "reports.html",
        request, context
    )
