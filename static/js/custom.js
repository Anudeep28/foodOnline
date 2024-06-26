let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        //console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address':address}, function(results, status){
        console.log('results :', results);
        console.log('status :', status);
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);
            
            

        }
    });

    // Loop through address and fill the vars
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            
            // console.log("country :",place.address_components[i].types[j].long_name);
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // State
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // City
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // Pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pincode').val(place.address_components[i].long_name);
            }else{
                $('#id_pincode').val("");
            }
        }

        }
}


/////////////////////////////////// This for the Cart Functionality ///////////////////////////
$(document).ready(function(){
    
    // add to cart
    $('.add_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        
        $.ajax({
            type: 'GET',
            url: url,
            success:function(response){
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, "", "info").then(function() {
                        window.location = '/accounts/userLogin/';
                        
                    })
                }else if (response.status == 'Failed') {
                    swal(response.message, "", "error")
                }else{
                    $('#cart_counter').html(response.cart_count['cart_count']);
                    $('#qty-'+food_id).html(response.quantity);

                    // Subtotal and Total
                    applyCartAmount(response.cart_amount['subtotal'], 
                                    response.cart_amount['tax_dict'], 
                                    response.cart_amount['grand_total']);
                }
                
            }
        })
    })


    // Place the cart item quantities on load
    $('.item-qty').each(function(){
        var the_id = $(this).attr('id')
        var quantity = $(this).attr('data-qty')
        $('#'+the_id).html(quantity)
    })

    // decrease the cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');
        
        $.ajax({
            type: 'GET',
            url: url,
            success:function(response){
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, "", "info").then(function(){
                        window.location = '/accounts/userLogin/';
                        
                    })
                }else if (response.status == 'Failed') {
                    swal(response.message, "", "error")
                }else{
                    $('#cart_counter').html(response.cart_count['cart_count']);
                    $('#qty-'+food_id).html(response.quantity);
                    // The path should always be th eexact
                    if (window.location.pathname == '/marketplace/cartView/'){
                    removeCartItem(response.quantity, cart_id);
                    checkEmptyCart();
                    // Subtotal and Total
                    applyCartAmount(response.cart_amount['subtotal'], 
                                    response.cart_amount['tax_dict'], 
                                    response.cart_amount['grand_total']);
                    }
                    
                }
                
            }
                
        })
    })




    // Delete the cart
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,
            success:function(response){
                console.log(response)
                if (response.status == 'Failed') {
                    swal(response.message, "", "error")
                }else{
                    $('#cart_counter').html(response.cart_count['cart_count']);
                    
                    swal(response.status, response.message, 'success')
                    
                    

                    removeCartItem(0, cart_id);
                    checkEmptyCart()
                    
                    // Subtotal and Total
                    applyCartAmount(response.cart_amount['subtotal'], 
                    response.cart_amount['tax_dict'], 
                    response.cart_amount['grand_total']);
                    //removeCartItem(0, cart_id);
                }
                }
                
        })
    })

    // delete the cart item if quantity is zero
    function removeCartItem(cartItemQty, cart_id){
        
            if(cartItemQty <= 0){
                document.getElementById("cart-item-"+cart_id).remove()
            }
        
        
    }

    // Check if the cart is empty
    function checkEmptyCart(){
        var cart_count = document.getElementById('cart_counter').innerHTML
        if (cart_count == 0){
            document.getElementById('empty-cart').style.display = "block";
        }
    }

    

    // Apply cart amounts 
    function applyCartAmount(subtotal, tax_dict, grand_total){
         // this should be only run whe th user is in cart menu
        if (window.location.pathname == '/marketplace/cartView/'){
            $('#subtotal').html(subtotal)
            $('#total').html(grand_total)
            for (key1 in tax_dict) {
                for(key2 in tax_dict[key1]){
                    $('#tax-'+key1).html(tax_dict[key1][key2])
                }
            }
        }
        
    }

    // Document opening hours updater
    // here we taking in the class of the element
    $('.add_hour').on('click', function(e) {
        e.preventDefault();
        // retrieveing the selected form values
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hours').value
        var to_hour = document.getElementById('id_to_hours').value
        
        var url = document.getElementById('add_Opening_Hours').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        console.log('Add part :',day, from_hour, to_hour, is_closed, csrf_token, url)
        
        if (is_closed) {
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }
        
        if (eval(condition)) {
            $.ajax({
                type:'POST',
                url:url,
                data:{
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },
                success: function(response){
                    if (response.status == 'success') {
                        if (response.is_closed == 'Closed') {
                            console.log('id :',response.id)
                            html='<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/vendor/deleteOpeningHours/'+response.id+'/">Remove</a></td></tr>'
                            // $('.opening_hours').append(html)
                            // document.getElementById('opening_hours').reset();
                        } else {
                            html='<tr id="hour-'+response.id+'" ><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/deleteOpeningHours/'+response.id+'/">Remove</a></td></tr>'
                               
                        }
                        $('.opening_hours').append(html)
                        document.getElementById('opening_hours').reset(); 
                        
                    } else {
                        swal(response.message,'','error')
                    }
                }
            })
        } else {
            swal('Please fill all the fields',"",'info')
        }
        
    });

    // REmove the opening hours
    $(document).on('click','.remove_hour', function(e) {
        e.preventDefault();
        url = $(this).attr('data-url');
            console.log('url :',url)
        $.ajax({
            type:'GET',
            url:url,
            success: function(response) {
                if (response.status == 'success') {
                    document.getElementById('hour-'+response.id).remove()
                }
                
            }
        })
    })
    // Document ready closing brackets below

});