// Copyright (c) 2021, Real Experts GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("Catch Log Entry", {
	onload: (frm) => {
		if (frm.is_new() && !frm.doc.year) {
			frm.set_value("year", moment().year() - 1);
		}
	},
	refresh: (frm) => {
		if (frm.doc.docstatus == 0 && !frm.is_new())	{
			frm.add_custom_button(__("New Catch Log Entry"), () => {
				frappe.new_doc(frm.doctype, {
					organization: frm.doc.organization,
					year: frm.doc.year,
				});
			});
	   }
   },
});
