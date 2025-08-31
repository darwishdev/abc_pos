import json
import os
import frappe
from pathlib import Path
from abc_utils.utils.customfield_utils import install_custom_fields
from abc_utils.utils.sql_utils import run_sql
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
SQL_DIR = Path(frappe.get_app_path("abc_pos", "abc_pos", "sql"))
CUSTOMFIELDS_PATH = os.path.join(frappe.get_app_path("abc_pos"), "setup", "customfields")
DEBUG = os.environ.get("BENCH_DEBUG", "").lower() in {"1", "true", "yes"}



def after_install():
	return {"ok": True}

def after_migrate():
    install_custom_fields(CUSTOMFIELDS_PATH)
    run_sql(SQL_DIR)


