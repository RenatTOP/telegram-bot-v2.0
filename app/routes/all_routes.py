import aiohttp_jinja2
from aiohttp import web


async def dashboard(request: web.Request):
    context = {"page": "dashboard"}
    return await aiohttp_jinja2.render_template_async(
        "dashboard.html", request, context
    )


async def products(request: web.Request):
    context = {"page": "products"}
    return await aiohttp_jinja2.render_template_async(
        "products.html",
        request, context
    )

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
    