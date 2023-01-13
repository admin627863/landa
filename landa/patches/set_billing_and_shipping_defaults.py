import frappe
from frappe.query_builder import DocType


def execute():
	set_billing_and_shipping_defaults()
	cleanup_addresses()


def set_billing_and_shipping_defaults():
	Address = DocType("Address")
	DynamicLink = DocType("Dynamic Link")

	addresses = (
		frappe.qb.from_(Address)
		.inner_join(DynamicLink)
		.on(Address.name == DynamicLink.parent)
		.select(
			Address.name,
			Address.is_shipping_address,
			Address.is_primary_address,
			DynamicLink.link_name,
		)
		.where((Address.is_shipping_address == 1) | (Address.is_primary_address == 1))
		.where(DynamicLink.link_doctype == "Customer")
		.run()
	)

	for address_name, is_shipping, is_primary, customer in addresses:
		if is_primary:  # billing address
			contact = frappe.get_all(
				"Contact", [["name", "like", address_name.replace(" ", "%")]], pluck="name"
			)

			frappe.db.set_value(
				"Customer",
				customer,
				{
					"default_billing_contact": contact[0] if contact else None,
					"default_billing_address": address_name,
				},
			)

		if is_shipping:
			contact = frappe.get_all(
				"Contact", [["name", "like", address_name.replace(" ", "%")]], pluck="name"
			)

			frappe.db.set_value(
				"Customer",
				customer,
				{
					"default_shipping_contact": contact[0] if contact else None,
					"default_shipping_address": address_name,
				},
			)


def cleanup_addresses():
	# the two checkboxes are no longer used and are hidden from now on.
	frappe.db.sql(
		"""update `tabAddress` set is_shipping_address=0, is_primary_address=0"""
	)
