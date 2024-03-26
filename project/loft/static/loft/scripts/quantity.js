const quantity = document.getElementById('quantity_input')
const successBtn = document.getElementById('success')
const quant = document.getElementById('quant')

successBtn.onclick = function () {
    quant.textContent = Number(quantity.value);
}




