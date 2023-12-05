let updateCart = document.getElementsByClassName('add-cart')

for (let i = 0; i< updateCart.length; i++){
    updateCart[i].addEventListener('click', function(){
        let inventoryId = this.dataset.inventory
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('inventoryId:', inventoryId, 'action:', action, 'productId:', productId)
        console.log('User:', user)
        
        if(user){
            UpdateUserCart(inventoryId, action, productId)
        }
    })
}

// write a function that takes compares the inventory id to the product_number and the use the data-action attribute to add
// the item to the cart, so whenever the barcode scanner scans the product, the product with that product_number
// exist in the database, the item is added to the cart.

// let scanCart = document.getElementsByClassName()

function UpdateUserCart(inventoryId, action, productId){
    console.log('Sending data')

    let url = '/update_cart/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'inventoryId':inventoryId, 'action':action, 'productId':productId})
    })
    .then(res => res.json())
    .then((data) =>{
        console.log('data:', data)
        document.getElementById('addCart').innerHTML = `${data.qty}`
    })
}

let scanCart = document.getElementsByClassName('scan-cart')

for (let i = 0; i< scanCart.length; i++){
    scanCart[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('User:', user)
        
        if(user){
            UpdateUserCart(productId, action)
        }
    })
}

function ScanUserCart(productId, action){
    console.log('Sending data')

    let url = '/scan_cart/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then(res => res.json())
    .then((data) =>{
        console.log('data:', data)
        document.getElementById('addCart').innerHTML = `${data.qty}`
    })
}


let inputfields = document.getElementsByClassName('Qty')
for(i = 0; i < inputfields.length; i++){
    inputfields[i].addEventListener('change', updateQuantity)   
    
}

function updateQuantity(e){
    let inputvalue = e.target.value
    let inventoryId = e.target.dataset.inventory

    const data = {invent_id: inventoryId, val: inputvalue};
    let url = '/update_quantity/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify(data)
    })
    .then(res => res.json())

    .then((data) =>{
        console.log('Success:', data);
        document.getElementById('sub_total').innerHTML = `${data.sub_total.toFixed(1)}`
        document.getElementById('final_total').innerHTML = `<b>Total:</b><div><i class="fa-solid fa-naira-sign"></i>${data.final_total.toFixed(1)}</div>`
        document.getElementById('sum_quantity').innerHTML = `<b>Item:</b><div>${data.total_quantity}</div>`
        document.getElementById('addCart').innerHTML = `${data.total_quantity}`
        location.reload()
    })
};