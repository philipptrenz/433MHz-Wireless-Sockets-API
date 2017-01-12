let secret = 'test';

$( document ).ready(function() {
	loadDevices();

	$('input').on( "keyup", function() {
		var device = $('#new-device-id').val();
		var name = $('#new-device-name').val();
		if (/^([01]{5}[A-G])$/.test(device) &&  name.length != 0) {
			console.log('input valid');
			$('#add-button').attr("disabled", false);
		} else {
			$('#add-button').attr("disabled", true);
		}
	});

});
var responseArray;
function loadDevices() {
	console.log('loading list of devices ...')
	$.ajax({
        type: "POST",
        url: "/list",
        async: true,
        data: JSON.stringify({ secret: secret }),
        contentType: "application/json",
        complete: function (data) {
        	responseArray = data.responseJSON;
        	$('#switch-table').empty();

        	for (var i=0; i<responseArray.length; i++){
        		var device = responseArray[i].device
        		var name = responseArray[i].name
        		var state = responseArray[i].state
        		var html = '<div class="row"><div class="cell">'+name+'</div><div class="cell"><div class="switch"><label><input type="checkbox" class="device-switches" id="'+device+'"><span class="lever"></span></label></div></div></div>';
        		$('#switch-table').append(html);
        		$('#'+device).prop('checked', state == 'on' ? true : false);
        	}
        	wait = false;
        	/* Button event */
			$('input.device-switches').on('change', function() {
				if ($(this).prop('checked')) {
					$.get($(this).attr('id')+'/on');
				} else {
					$.get($(this).attr('id')+'/off');
				}
			});
			console.log(responseArray.length+" devices loaded");
    	}
	});
}

var isSettings = false;
function settings() {
	isSettings = !isSettings;
	if (isSettings) {
		$('#settings-button').html('replay');
		$('#new-switch-form').show();
		loadDevicesSettings();
	} else {
		$('#settings-button').html('settings');
		$('#new-switch-form').hide();
		loadDevices();
	}
}

function remove(device) {
	$.ajax({
        type: "POST",
        url: "/"+device+"/remove",
        async: true,
        data: JSON.stringify({ secret: secret }),
        contentType: "application/json",
        complete: function (data) {
        	if (data.status == 200) {
        		console.log(device+' sucessfully deleted');
        		loadDevicesSettings();
        	}
    	}
	});
}

function addNewSwitch(){
	var device = $('#new-device-id').val();
	var name = $('#new-device-name').val();

	$.ajax({
        type: "POST",
        url: "/"+device+"/add",
        async: true,
        data: JSON.stringify({ secret: secret, name: name}),
        contentType: "application/json",
        complete: function (data) {
        	if (data.status == 200) {
        		console.log(device+' sucessfully deleted');
        		loadDevicesSettings();
        	}
    	}
	});

	$('#new-device-id').val('');
	$('#new-device-name').val('');
	$('#add-button').attr("disabled", true);
}

function loadDevicesSettings(){
	console.log('loading list of devices for settings ...')
	$.ajax({
        type: "POST",
        url: "/list",
        async: true,
        data: JSON.stringify({ secret: secret }),
        contentType: "application/json",
        complete: function (data) {
        	responseArray = data.responseJSON;
        	$('#switch-table').empty();

        	for (var i=0; i<responseArray.length; i++){
        		var device = responseArray[i].device
        		var name = responseArray[i].name
        		var state = responseArray[i].state
        		var oldSwitches = '<div class="row device-settings" id="'+device+'"><div class="cell"><div class="input-field">'+device+'</div></div><div class="cell"><div class="input-field">'+name+'</div></div><div class="cell"><a class="btn-floating btn-medium red accent-1" type="submit" onclick="remove(\''+device+'\')"><i class="material-icons">delete</i></a></div></div>';
    			$('#switch-table').append(oldSwitches);
        	}
        	wait = false;
    	}
	});
}