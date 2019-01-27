// Copyright (c) 2019, Si Hay Sistema and contributors
// For license information, please see license.txt

function compartir_item(frm, doctype, codigo) {
    // Agrega un boton llamado share
    frm.add_custom_button(__('Share'), function () {
        // Llama al metodo python para obtener un listado con los
        // usuarios configurados
        frappe.call({
            method: "jsonshare.utils.obtener_usuarios",
            callback: function (response) {
                // Crea un Modal(dialogo), en las opciones del campo
                // user_share se asigna el listado de usarios retornados
                let dialog = new frappe.ui.Dialog({
                    title: __('Compartir Item'),
                    fields: [
                        {
                            fieldtype: 'Select',
                            fieldname: 'user_share',
                            label: __('Seleccione Usuario'),
                            reqd: true,
                            options: response.message,
                            description: __('Seleccione el host/usuario con quien quiera compartir el Item')
                        },
                        {
                            fieldtype: 'Button',
                            fieldname: 'btn_share',
                            label: __('Compartir'),
                            options: '',
                            description: __(''),
                        }
                    ]
                });

                // Muestra el dialogo
                dialog.show();

                // Agrega un event lister al boton compartir del dialogo
                dialog.fields_dict.btn_share.$wrapper.on('click', function (e) {
                    // console.log('Eso es');
                    // Imprime el valor seleccionado
                    console.log(dialog.fields_dict.user_share.value);
                    // Imprime el codigo del item a ser enviado
                    //console.log(frm.doc.item_code);
                    frappe.call({
                        method: "jsonshare.api_data.obtener_datos",
                        args: {
                            item: codigo,
                            usuario: dialog.fields_dict.user_share.value,
                            doctype: doctype
                        },
                        callback: function () {
                            // frm.reload_doc();
                        }
                    });
                });
            }
        });

    }).addClass("btn-success");
}

frappe.ui.form.on("Item", {
    refresh: function (frm) {
        let item_code = frm.doc.item_code;
        compartir_item(frm, 'Item', item_code);
    }
});

frappe.ui.form.on("Customer", {
    refresh: function (frm) {
        let customer_name = frm.doc.customer_name;
        compartir_item(frm, 'Customer', customer_name);
    }
});

frappe.ui.form.on("Supplier", {
    refresh: function (frm) {
        let supplier_name = frm.doc.supplier_name;
        compartir_item(frm, 'Supplier', supplier_name);
    }
});