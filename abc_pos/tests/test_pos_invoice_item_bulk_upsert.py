# import frappe
# import unittest
#
# from abc_pos.abc_pos.api.pos_invoice import pos_invoice_item_bulk_upsert
# class TestPOSBulkInsert(unittest.TestCase):
#     def setUp(self):
#
#         # --- Setup same as before ---
#         if not frappe.db.exists("Company", "_Test Company"):
#             frappe.get_doc({
#                 "doctype": "Company",
#                 "company_name": "_Test Company",
#                 "abbr": "_TC",
#                 "default_currency": "USD",
#             }).insert()
#
#         root_wh = frappe.db.get_value("Warehouse", {"is_group": 1, "company": "_Test Company"})
#         if not root_wh:
#             root_wh = frappe.get_doc({
#                 "doctype": "Warehouse",
#                 "warehouse_name": "_Test Company",
#                 "company": "_Test Company",
#                 "is_group": 1
#             }).insert().name
#
#         if not frappe.db.exists("Warehouse", "_Test Warehouse - _TC"):
#             frappe.get_doc({
#                 "doctype": "Warehouse",
#                 "warehouse_name": "_Test Warehouse",
#                 "company": "_Test Company",
#                 "parent_warehouse": root_wh,
#                 "is_group": 0
#             }).insert()
#
#         if not frappe.db.exists("Account", "Write Off - _TC"):
#             parent = frappe.db.get_value("Account", {"root_type": "Expense", "company": "_Test Company"})
#             frappe.get_doc({
#                 "doctype": "Account",
#                 "account_name": "Write Off",
#                 "company": "_Test Company",
#                 "parent_account": parent,
#                 "root_type": "Expense",
#                 "report_type": "Profit and Loss"
#             }).insert()
#
#         root_cc = frappe.db.get_value("Cost Center", {"is_group": 1, "company": "_Test Company"})
#         if not root_cc:
#             root_cc = frappe.get_doc({
#                 "doctype": "Cost Center",
#                 "cost_center_name": "_Test Company",
#                 "company": "_Test Company",
#                 "is_group": 1
#             }).insert().name
#
#         # Ensure a child cost center
#         if not frappe.db.exists("Cost Center", "Main - _TC"):
#             frappe.get_doc({
#                 "doctype": "Cost Center",
#                 "cost_center_name": "Main",
#                 "company": "_Test Company",
#                 "is_group": 0,
#                 "parent_cost_center": root_cc,   # always set explicitly
#             }).insert()
#         if not frappe.db.exists("Mode of Payment", "Cash"):
#             frappe.get_doc({
#                 "doctype": "Mode of Payment",
#                 "mode_of_payment": "Cash",
#                 "type": "Cash"
#             }).insert()
#
#         if not frappe.db.exists("Customer", "_Test Customer"):
#             frappe.get_doc({
#                 "doctype": "Customer",
#                 "customer_name": "_Test Customer",
#                 "customer_group": "All Customer Groups",
#                 "territory": "All Territories"
#             }).insert()
#
#         if not frappe.db.exists("POS Profile", "Test POS Profile"):
#             frappe.get_doc({
#                 "doctype": "POS Profile",
#                 "name": "Test POS Profile",
#                 "company": "_Test Company",
#                 "customer": "_Test Customer",
#                 "warehouse": "_Test Warehouse - _TC",
#                 "write_off_account": "Write Off - _TC",
#                 "write_off_cost_center": "Main - _TC",
#                 "payments": [
#                     {"mode_of_payment": "Cash", "default": 1}
#                 ],
#             }).insert()
#  # Create a fresh invoice for this test run
#         self.invoice = frappe.get_doc({
#             "doctype": "POS Invoice",
#             "customer": "_Test Customer",
#             "pos_profile": "Test POS Profile",
#             "docstatus": 0
#         }).insert()
#
#     def test_bulk_upsert_invoice_items(self):
#         # Prepare test items
#         items = [
#             {
#                 "item_code": "Burger",
#                 "item_name": "Burger",
#                 "uom": "Unit",
#                 "qty": 2,
#                 "rate": 50,
#                 "amount": 100,
#                 "folio_window": "1"
#             },
#             {
#                 "item_code": "B52",
#                 "item_name": "B52",
#                 "uom": "Unit",
#                 "qty": 1,
#                 "rate": 120,
#                 "amount": 120,
#                 "folio_window": "2"
#             }
#         ]
#
#         # Call API
#         result = pos_invoice_item_bulk_upsert(self.invoice.name, items)
#
#         # Assert response
#         self.assertTrue(result["ok"])
#         self.assertEqual(result["invoice_id"], self.invoice.name)
#         self.assertEqual(result["count"], 2)
#         self.assertEqual(result["total_qty"], 3.0)
#         self.assertEqual(result["total_amount"], 220.0)
#
#         # Validate DB state
#         db_items = frappe.get_all(
#             "POS Invoice Item",
#             filters={"parent": self.invoice.name},
#             fields=["item_code", "qty", "rate", "base_amount"]
#         )
#         self.assertEqual(len(db_items), 2)
#
#         burger = next(i for i in db_items if i["item_code"] == "Burger")
#         self.assertEqual(float(burger["qty"]), 2.0)
#         self.assertEqual(float(burger["base_amount"]), 100.0)
#
#         b52 = next(i for i in db_items if i["item_code"] == "B52")
#         self.assertEqual(float(b52["qty"]), 1.0)
#         self.assertEqual(float(b52["base_amount"]), 120.0)
#
#     def tearDown(self):
#         # Remove invoice first
#         if self.invoice and frappe.db.exists("POS Invoice", self.invoice.name):
#             frappe.delete_doc("POS Invoice", self.invoice.name, force=True, ignore_permissions=True)
#
#         # Remove test records in reverse dependency order
#         for dt, name in [
#             ("POS Profile", "Test POS Profile"),
#             ("Customer", "_Test Customer"),
#             ("Mode of Payment", "Cash"),
#             ("Warehouse", "_Test Warehouse - _TC"),
#             ("Account", "Write Off - _TC"),
#             ("Cost Center", "Main - _TC"),
#             ("Warehouse", "_Test Company - _TC"),  # ✅ this is the root warehouse, not a company
#             ("Company", "_Test Company"),
#         ]:
#             if frappe.db.exists(dt, name):
#                 frappe.delete_doc(dt, name, force=True, ignore_permissions=True)
#
#         frappe.db.commit()
