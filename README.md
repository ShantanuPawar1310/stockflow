# StockFlow – B2B Inventory Management System

StockFlow is a multi-tenant B2B SaaS platform that helps companies manage products
across multiple warehouses, track inventory changes, and generate low-stock alerts
with supplier information for reordering.

This repository represents a backend-focused case study demonstrating API design,
database modeling, and production-ready thinking.

---

## Core Features

- Product management with global SKU uniqueness
- Multi-warehouse inventory tracking
- Inventory change audit trail
- Supplier linkage for reordering
- Low-stock alerts based on sales velocity
- Support for bundled products

---

## Tech Stack

- Language: Python
- Framework: Flask
- ORM: SQLAlchemy
- Database: MySQL
- Architecture: REST API

---

## Key Design Decisions

- Products are **warehouse-agnostic**
- Inventory is modeled via a **junction table**
- Monetary values use **DECIMAL**, not float
- All write operations use **atomic transactions**
- Inventory changes are fully auditable

---

## Assumptions

- SKU is globally unique across the platform
- Recent sales = last 30 days
- Each product has one primary supplier
- Low-stock threshold is defined per product

See `docs/assumptions.md` for details.

---

## Example Endpoint
GET /api/companies/{company_id}/alerts/low-stock
---

## Author

Shantanu S. Pawar  The case study file link https://docs.google.com/document/d/e/2PACX-1vT_8t-bOkjbVBP1FxHWNfyoHCe10e2o3Ghbhy9amidxmsUuJcA7d4PjQ1oVDJVFPsZBTxDWvOJLRpI6/pub
