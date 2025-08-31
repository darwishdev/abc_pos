import frappe
from frappe import _
from frappe.utils.password import check_password
from frappe.core.doctype.user.user import generate_keys
from frappe.utils.password import get_decrypted_password
from frappe.sessions import Session
from frappe.utils import random_string, now_datetime

@frappe.whitelist(allow_guest=True)
def cashier_login(cashier_code, cashier_password, remember_me=0):
    try:
        # 1. Find user linked to cashier_code
        user_name = frappe.db.get_value("User", {"cashier_code": cashier_code, "cashier_password" : cashier_password,"enabled": 1}, "name")
        if not user_name:
            frappe.throw(_("User Not Found"))

        # 2. Validate password
        # if not check_password(user_name, cashier_password, doctype="User", fieldname="password"):
        #     frappe.throw(_("Invalid cashier credentials"))
        #
        # 3. Get user document
        user_doc = frappe.get_doc("User", user_name)

        # 4. Generate API credentials if they don't exist
        api_key = user_doc.api_key
        api_secret = None

        if api_key:
            try:
                api_secret = get_decrypted_password("User", user_name, "api_secret")
            except:
                api_secret = None

        # Generate new API credentials if missing
        if not api_key or not api_secret:
            # Generate new API key and secret
            api_key = frappe.generate_hash(length=15)
            api_secret = frappe.generate_hash(length=15)

            # Update user document
            user_doc.api_key = api_key
            user_doc.api_secret = api_secret
            user_doc.save(ignore_permissions=True)
            frappe.db.commit()

        # 5. Create authorization token
        token_value = f"{api_key}:{api_secret}"


        return {
            "success": True,
            "authorization": token_value,
            "token_type": "token",
            "user": user_name,
            "full_name": user_doc.full_name,
            "message": "Login successful"
        }

    except Exception as e:
        # Log the error for debugging
        frappe.log_error(f"Cashier login failed: {str(e)}", "Cashier Login Error")

        # Return proper error response
        frappe.local.response["http_status_code"] = 401
        return {
            "success": False,
            "message": str(e),
            "timestamp": now_datetime(),
        }


@frappe.whitelist()
def get_session_info():
    """Get current session information for authenticated users"""
    if frappe.session.user == "Guest":
        frappe.throw(_("Not authenticated"), frappe.AuthenticationError)

    user_doc = frappe.get_doc("User", frappe.session.user)

    return {
        "success": True,
        "user": {
            "name": user_doc.name,
            "full_name": user_doc.full_name,
            "email": user_doc.email,
            "user_image": user_doc.user_image,
            "roles": frappe.get_roles(frappe.session.user),
            "cashier_code": user_doc.cashier_code,
            "language": user_doc.language or frappe.local.lang,
        },
        "session": {
            "sid": frappe.session.sid,
            "csrf_token": frappe.sessions.get_csrf_token(),
            "time_zone": frappe.db.get_system_setting("time_zone"),
            "currency": frappe.db.get_default("Currency"),
        },
        "timestamp": now_datetime(),
    }

@frappe.whitelist()
def cashier_logout():
    """Logout current user and destroy session"""
    if frappe.session.user == "Guest":
        return {"success": True, "message": _("Already logged out")}

    try:
        # Destroy the session
        frappe.local.login_manager.logout()

        # Clear cookies
        frappe.local.cookie_manager.delete_cookie("sid")
        frappe.local.cookie_manager.delete_cookie("csrf_token")

        return {
            "success": True,
            "message": _("Logout successful"),
            "timestamp": now_datetime(),
        }
    except Exception as e:
        frappe.log_error(f"Cashier logout failed: {str(e)}", "Cashier Logout Error")
        return {
            "success": False,
            "message": str(e),
            "timestamp": now_datetime(),
        }
