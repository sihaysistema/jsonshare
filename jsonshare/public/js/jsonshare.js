console.log('Hola');

frappe.ui.form.on("Item", {
    refresh: function (frm, cdt, cdn) {
        frm.add_custom_button(__('Share'), function () {

            let dialog = new frappe.ui.Dialog({
                title: __('Compartir Item'),
                fields: [
                    {
                        fieldtype: 'Select',
                        fieldname: 'user_share',
                        label: __('Seleccione Usuario'),
                        options: 'Hola Mundo',
                        description: __(""),
                        // options: rendered_template
                    },
                    {
                        fieldtype: 'Button',
                        fieldname: 'btn_share',
                        label: __('Compartir'),
                        options: '',
                        description: __(""),
                        // options: rendered_template
                    }
                ]
            });

            dialog.show();

            dialog.fields_dict.btn_share.$wrapper.on('click', function (e) {
                console.log('Eso es');
                // frappe.call({
                //     method: "jsonshare.api.crud",
                //     args: {
                //         item: frm.doc.item_code
                //     },
                //     callback: function () {
                //         // frm.reload_doc();
                //     }
                // });
            });

        }).addClass("btn-primary");
    }
});