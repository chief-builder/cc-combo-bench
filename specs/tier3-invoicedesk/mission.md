Mission

InvoiceDesk is a small invoicing tracker for a one-person business.

"Bill it. Send it. Get paid."

Built as a learning project for course students exploring AI coding agents, InvoiceDesk demonstrates a real (if tiny) multi-entity application: invoices and the payments recorded against them, a lifecycle the server actually enforces (you can't mark an invoice paid until the money has arrived), a billing-stats page with real money math, and a JSON API alongside the HTML pages — still FastAPI, Jinja2 templates, and Bootstrap CSS, still no database and no authentication, everything in memory.

The site: a home page, an invoice board filterable by status, invoice detail pages with payment history and balance due, forms to create invoices and record payments, buttons that move an invoice through its lifecycle (and refuse illegal or premature moves), a stats dashboard, and an API endpoint for anything that would rather skip the HTML.
