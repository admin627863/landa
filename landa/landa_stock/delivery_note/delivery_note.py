import frappe
from frappe import _


def validate(delivery_note, event):
	"""Validate that only returnable items are returned."""
	if delivery_note.is_return:
		for item in delivery_note.items:
			if frappe.db.get_value("Item", item.item_code, "cannot_be_returned"):
				frappe.throw(_("Item {} cannot be returned").format(item.item_name))
				return
	elif not frappe.has_permission(ptype="submit", doc=delivery_note):
		frappe.throw(
			"""Nur der Regionalverband darf Lieferscheine für Lieferungen anlegen. Vereine dürfen Lieferscheine für Retouren aus im System gebuchten Lieferungen erzeugen. Dazu zur <a href="/app/delivery-note">Liste aller Lieferungen</a> wechseln, die Lieferung aufrufen und oben rechts unter "Erstellen" > "Retoure" auswählen."""
		)


def on_submit(delivery_note, event):
	"""Auto-create Sales Invoice for Delivery Note."""
	# 2021-09-24: disabled for now, but kept in case preferences change in the future

	# from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
	#
	# if delivery_note.get('create_sales_invoice'):
	#	sales_invoice = make_sales_invoice(delivery_note.get('name'))
	#	sales_invoice.save()
	#	sales_invoice.submit()
	pass


def autoname(doc, event):
	"""Create Company-specific Delivery Note name."""
	from landa.utils import get_new_name

	if doc.is_return:
		doc.name = get_new_name("RET", doc.company, "Delivery Note")
	else:
		doc.name = get_new_name("LIEF", doc.company, "Delivery Note")
