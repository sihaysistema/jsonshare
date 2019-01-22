console.log('Hola');

frappe.ui.form.on("Item", {
    refresh: function (frm, cdt, cdn) {
        // Agrega un boton llamado share
        frm.add_custom_button(__('Share'), function () {

            // Llama al metodo python para obtener un listado con los
            // usuarios configurados
            frappe.call({
                method: "jsonshare.utils.obtener_usuarios",
                callback: function (r) {
                    // console.log(r.message);
                    // Crea un Modal(dialogo), en las opciones del campo
                    // user_share se asigna el listado de usarios retornados
                    let dialog = new frappe.ui.Dialog({
                        title: __('Compartir Item'),
                        fields: [
                            {
                                fieldtype: 'Select',
                                fieldname: 'user_share',
                                label: __('Seleccione Usuario'),
                                options: r.message,
                                description: __('Seleccione el host/usuario con quien quiera compartir el Item'),
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
                        console.log('Eso es');
                        // Imprime el valor seleccionado
                        console.log(dialog.fields_dict.user_share.value);
                        // Imprime el codigo del item a ser enviado
                        console.log(frm.doc.item_code);
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
                }
            });

        }).addClass("btn-success");
    }
});