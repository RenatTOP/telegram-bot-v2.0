from app.routes.all_routes import dashboard, products, departments, invoices, reports


def routes(app):
    app.router.add_get("/", dashboard, name='dashboard')
    app.router.add_route("*", "/products", products, name='products')
    app.router.add_get("/departments", departments, name='departments')
    app.router.add_get("/invoices", invoices, name='invoices')
    app.router.add_get("/reports", reports, name='reports')


