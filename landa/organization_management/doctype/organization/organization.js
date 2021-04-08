// Copyright (c) 2021, Landesverband Sächsischer Angler e. V.Real Experts GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Organization', {
    refresh: function(frm) {
        // Automatically add the backlink to Organization when a new Address or
        // Contact is added.
        frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Organization' };

        // Display Address and Contact only after the Member has been created,
        // not on the initial form.
        frm.toggle_display(['section_address_and_contact'], !frm.doc.__islocal);

        if (frm.doc.__islocal) {
            frappe.contacts.clear_address_and_contact(frm);
        }
        else {
            frappe.contacts.render_address_and_contact(frm);
        }
    },
});