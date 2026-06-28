function changeAmount(addition, id) {
    let productRow = document.getElementById('product_row_' + id)
    let amountInput = productRow.querySelector(".amount_product")
    let oldValue = Number(amountInput.value)
    let newValue = oldValue + addition
    let price = Number(productRow.querySelector(".price").innerHTML)
    let costElem = productRow.querySelector(".cost")
    if (newValue > 0) {
        amountInput.value = newValue;
    } else {
        amountInput.value = 1;
        newValue = 1
    }

    if (oldValue != newValue) {
        fetch('/recount-product/', {
            method: "POST",
            headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
            body: JSON.stringify({id: id, newAmount: newValue})
        })
            .then(response => response.json())
            .then(data => {
                costElem.innerHTML = Math.round(price * newValue * 100) / 100
                getTotalPrice();
            })
            .catch(error => console.error("Ошибка:", error));
    }
}

function deleteProduct(id) {
    document.getElementById('cart_loader_' + id).style.display = 'inline-block'
    document.getElementById('trash_img_' + id).style.display = 'none'
    fetch('/delete-product/' + id + '/')
        .then(res => res.ok ? res : Promise.reject(res))
        .then(response => response.json())
        .then(commits => {
            document.querySelector('#product_row_' + id).remove();
            getTotalPrice();
            let product_rows = document.querySelectorAll('.product_row')
            for (let i = 0; i < product_rows.length; i++) {
                product_rows[i].querySelector('td').innerText = String(i + 1)
            }
            if (!countTableRows()) {
                if (document.getElementById('cart_table')) {
                    document.getElementById('cart_table').style.display = 'none'
                }
                if (document.getElementById('get_blank_button')) {
                    document.getElementById('get_blank_button').style.display = 'none'
                }
                if (document.getElementById('cart_info_text')) {
                    document.getElementById('cart_info_text').style.display = 'none'
                }
                if (document.getElementById('cart_info_text_not_enough')) {
                    document.getElementById('cart_info_text_not_enough').style.display = 'none'
                }
                if (document.getElementById('get_blank_button_not_enough')) {
                    document.getElementById('get_blank_button_not_enough').style.display = 'none'
                }
                if (document.getElementById('add_first_blank')) {
                    document.getElementById('add_first_blank').style.display = 'none'
                }
                if (document.getElementById('get_blank_button_empty_blanks')) {
                    document.getElementById('get_blank_button_empty_blanks').style.display = 'none'
                }
                if (document.getElementById('empty_cart_block')) {
                    document.getElementById('empty_cart_block').style.display = 'block'
                }
            }
        })
}

function deleteBlank(id) {
    let loader = document.getElementById('cart_loader_' + id)
    if (loader) {
        loader.style.display = 'block'
        loader.style.margin = '0 auto'
        loader.style.height = '32px'
    }
    document.getElementById('trash_img_' + id).style.display = 'none'
    fetch('/delete-blank/' + id + '/')
        .then(res => res.ok ? res : Promise.reject(res))
        .then(response => response.json())
        .then(commits => {
            if (document.getElementById('blank_info_' + id)) {
                document.getElementById('blank_info_' + id).style.display = "none"
            }
            document.querySelector('#product_row_' + id).remove();
            if (!countTableRows()) {
                document.getElementById('cart_table').style.display = 'none'
                let spare = document.getElementById('first_blank_form_spare')
                if (spare) spare.style.display = 'block'
                let btn = document.getElementById('add_new_blank_header_button')
                if (btn) btn.style.display = 'none'
            }
        })
}

function downloadBlank() {
    let select_value = document.getElementById('file_blank_name').value
    if (select_value != '0' && select_value != '') {
        return true
    } else {
        document.getElementById('file_blank_name').style.border = "2px solid red"
        return false
    }
}

function countTableRows() {
    let tableRows = document.getElementsByClassName('product_row')
    return tableRows.length
}

function getTotalPrice() {
    let costsData = document.querySelectorAll('.cost')
    let total = 0
    for (let i = 0; i < costsData.length; i++) {
        total += Number(costsData[i].innerHTML)
    }
    let totalElem = document.getElementById('total')
    if (totalElem) {
        totalElem.innerText = (Math.round(total * 100) / 100) + " ¥"
    }
    return total
}

function showDotOptions(id) {
    let dotOptionsElem = document.getElementById('dot_options_' + id)
    let isOpentDotOptionsElem = window.getComputedStyle(dotOptionsElem).display === "block"

    const elements = document.querySelectorAll(".dot_options");
    elements.forEach(element => {
        element.style.display = "none";
    });

    if (!isOpentDotOptionsElem) {
        dotOptionsElem.style.display = "block"
    }
}

function closeDotOptions(id, event) {
    if (event) {
        event.stopPropagation()
    }
    let dotOptionsElem = document.getElementById('dot_options_' + id)
    if (dotOptionsElem) dotOptionsElem.style.display = "none"
}

function closeNewNameModal() {
    let bg = document.getElementById('transporetn_bg')
    let newNameModalElem = document.getElementById('new_name_modal')
    if (bg) bg.style.display = "none"
    if (newNameModalElem) newNameModalElem.style.display = "none"
}

function closeReNameModal() {
    let bg = document.getElementById('transporetn_bg')
    let reNameModalElem = document.getElementById('re_name_modal')
    if (bg) bg.style.display = "none"
    if (reNameModalElem) reNameModalElem.style.display = "none"
}

function showRenameModal(id) {
    document.getElementById('rename_cart_id').value = id
    let bg = document.getElementById('transporetn_bg')
    let reNameModalElem = document.getElementById('re_name_modal')
    bg.style.display = "flex";
    reNameModalElem.style.display = "block";
}

function createNewList() {
    let name = document.getElementById('new_list_name_input').value || 'Новый список'
    fetch('/manage-cart/', {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({action: 'new_list', name: name})
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                window.location.href = '/cart/?cart_id=' + data.id
            }
        })
}

function renameList() {
    let name = document.getElementById('rename_list_name_input').value
    let cart_id = document.getElementById('rename_cart_id').value
    if (!name) return
    fetch('/manage-cart/', {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({action: 'rename_list', name: name, cart_id: parseInt(cart_id)})
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                window.location.reload()
            }
        })
}

function duplicateList(id) {
    fetch('/manage-cart/', {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({action: 'duplicate_list', cart_id: id})
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                window.location.href = '/cart/?cart_id=' + data.id
            }
        })
}

function deleteList(id) {
    fetch('/manage-cart/', {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({action: 'delete_list', cart_id: id})
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                window.location.reload()
            }
        })
}

function getSelectedProducts() {
    const selectedProducts = document.querySelectorAll('input[name="product"]:checked');
    let selectedId = []
    selectedProducts.forEach(input => {
        selectedId.push(input.value);
    });
    return selectedId
}

function showChangePassword() {
    let elements = document.querySelectorAll('.change_password');
    elements.forEach(element => {
        element.style.display == 'block' ? element.style.display = 'none' : element.style.display = 'block'
    });
}

function checkForm() {
    let psw = document.getElementById('new_password')
    let psw_repeat = document.getElementById('confirm_password')
    if (psw && psw_repeat && psw.value) {
        if (psw.value !== psw_repeat.value) {
            document.getElementById('psw_not_match').style.display = 'inline'
            return false
        }
    }
    return true
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const markerCheckbox = document.querySelector('input[name="marker"][value="mark_all"]');
    if (markerCheckbox) {
        markerCheckbox.addEventListener('change', function (event) {
            event.stopPropagation()
            const isChecked = markerCheckbox.checked;
            document.querySelectorAll('input[name="product"]').forEach(cb => cb.checked = isChecked);
            let optionsDiv = document.getElementById('options_container')
            if (optionsDiv) {
                optionsDiv.style.display = isChecked ? "flex" : "none"
            }
        });
    }

    document.querySelectorAll('input[name="product"]').forEach(function (productCheckbox) {
        productCheckbox.addEventListener('change', function () {
            let atLeastOneChecked = document.querySelectorAll('input[name="product"]:checked').length > 0;
            let optionsDiv = document.getElementById('options_container')
            if (optionsDiv) {
                optionsDiv.style.display = atLeastOneChecked ? "flex" : "none"
            }
        })
    });

    const moveToBtn = document.getElementById('moveTo')
    if (moveToBtn) {
        moveToBtn.addEventListener('click', function () {
            document.getElementById('options_container').style.display = "none"
            document.getElementById('move_container').style.display = "block"
        })
    }

    const moveToExec = document.getElementById('moveToExec')
    if (moveToExec) {
        moveToExec.addEventListener("click", function () {
            let checkedProductValues = getSelectedProducts()
            let selectedDestination = document.getElementById('destinationCartSelect').value;
            fetch('/manage-cart/', {
                method: 'POST',
                headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
                body: JSON.stringify({action: 'move_products', destination_cart: parseInt(selectedDestination), products: checkedProductValues.map(Number)})
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'ok') window.location.reload()
                })
        });
    }

    const deleteFromList = document.getElementById('deleteFromList')
    if (deleteFromList) {
        deleteFromList.addEventListener('click', () => {
            let selectedProducts = getSelectedProducts()
            fetch('/manage-cart/', {
                method: "POST",
                headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
                body: JSON.stringify({action: 'delete_products', products: selectedProducts.map(Number)})
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'ok') window.location.reload()
                });
        })
    }

    let timeoutMoveUpDownId;
    const moveUpBtn = document.getElementById('moveUp')
    if (moveUpBtn) {
        moveUpBtn.addEventListener('click', function () {
            const selectedRows = []
            document.querySelectorAll('input[name="product"]:checked').forEach(input => {
                selectedRows.push(input.parentNode.parentNode)
            })
            selectedRows.forEach(function (selectedRow) {
                let previousRow = selectedRow.previousElementSibling;
                if (previousRow && previousRow.classList.contains('product_row')) {
                    selectedRow.parentNode.insertBefore(selectedRow, previousRow);
                }
            })
            clearTimeout(timeoutMoveUpDownId);
            timeoutMoveUpDownId = setTimeout(saveNewOrder, 2000);
        })
    }

    const moveDownBtn = document.getElementById('moveDown')
    if (moveDownBtn) {
        moveDownBtn.addEventListener('click', function () {
            const selectedRows = []
            document.querySelectorAll('input[name="product"]:checked').forEach(input => {
                selectedRows.push(input.parentNode.parentNode)
            })
            selectedRows.reverse().forEach(function (selectedRow) {
                let nextRow = selectedRow.nextElementSibling;
                if (nextRow && nextRow.classList.contains('product_row')) {
                    selectedRow.parentNode.insertBefore(nextRow, selectedRow);
                }
            })
            clearTimeout(timeoutMoveUpDownId);
            timeoutMoveUpDownId = setTimeout(saveNewOrder, 2000);
        })
    }

    function saveNewOrder() {
        let productRows = document.querySelectorAll('.product_row')
        let newOrder = {}
        let i = 1;
        productRows.forEach(row => {
            let product_id = row.querySelector('input[name="product"]').value
            newOrder[i] = parseInt(product_id)
            i++
        })
        fetch('/manage-cart/', {
            method: "POST",
            headers: {"Content-Type": "application/json", "X-CSRFToken": getCookie('csrftoken')},
            body: JSON.stringify({action: 'reorder', new_order: newOrder})
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('options_container').style.display = "none"
            })
    }

    const addNewList = document.getElementById('add_new_list')
    if (addNewList) {
        addNewList.addEventListener('click', function () {
            document.getElementById('transporetn_bg').style.display = "flex";
            document.getElementById('new_name_modal').style.display = "block";
        });
    }

    const addNewBlankHeader = document.getElementById('add_new_blank_header_button')
    if (addNewBlankHeader) {
        addNewBlankHeader.addEventListener('click', () => {
            document.getElementById('add_file').click()
        })
    }

    const addFile = document.getElementById('add_file')
    if (addFile) {
        addFile.addEventListener('change', function () {
            document.getElementById('getFile').submit()
        })
    }

    const fileBlankName = document.getElementById('file_blank_name');
    if (fileBlankName) {
        fileBlankName.addEventListener('change', () => {
            document.getElementById('file_blank_name').style.border = "none"
        })
    }
});
