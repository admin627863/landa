import frappe
from frappe import _


# def has_permission(doc, ptype, user):
#	if not doc.links and not frappe.db.get_single_value(
#		"System Settings", "apply_strict_user_permissions"
#	):
#		# No links and strict user permissions disabled
#		return True

#	for link in doc.links:
#		linked_doc = frappe.get_doc(link.link_doctype, link.link_name)
#		if frappe.has_permission(
#			link.link_doctype, ptype=ptype, doc=linked_doc, user=user
#		):
#			# We have permission on one linked doc
#			return True

#	# There are linked docs but we don't have permission on any of them
#	return False


def validate(doc, event):
	"""
	Set explicit links to Customer, LANDA Member and Organization in the parent
	doc, if they are found in the child table. This lets us apply user
	permissions on child table links to the parent doc.
	"""
	linked_doctypes = set(link.link_doctype for link in doc.links)
	mandatory_links = {"Company", "LANDA Member", "Organization", "Customer"}
	if not linked_doctypes.intersection(mandatory_links):
		frappe.msgprint(
			_("This document should be linked to at least one Company, LANDA Member, Organization or Customer")
		)

	doc.customer = ""
	doc.landa_member = ""
	doc.organization = ""

	for link in doc.links:
		if link.link_doctype == "Customer":
			doc.customer = link.link_name
			doc.organization = link.link_name

		if link.link_doctype == "LANDA Member":
			doc.landa_member = link.link_name
			doc.organization = link.link_name[:7]

		if link.link_doctype == "Organization":
			doc.organization = link.link_name