console.log('Hola');

frappe.ui.form.on("Item", {
    refresh: function (frm, cdt, cdn) {
        console.log('Hola mundo');
        frm.add_custom_button(__('Share'), function () {
            frappe.call({
                method: "jsonshare.api.crud",
                args: {
                    item: frm.doc.item_code
                },
                callback: function () {
                    // frm.reload_doc();
                }
            });
        }).addClass("btn-primary");
    }
});