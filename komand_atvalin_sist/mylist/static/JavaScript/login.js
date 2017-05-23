$(function(){
    $('#repeat-password-wrong').hide();
    $('#submit-signup').prop('disabled', true);
    $('#submit-login').prop('disabled', true);
});

$(document).ready(function (){
    if ($('#login-error-message').text().length) {$('#login-tab').click();}
});

$('.form').find('input, textarea').on('keyup blur focus', function (e) {

  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight');
			} else {
		    label.removeClass('highlight');
			}
    } else if (e.type === 'focus') {

      if( $this.val() === '' ) {
    		label.removeClass('highlight');
			}
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.signup-password-field-wrap').find('input, textarea').on('keyup blur focus', function (e) {

  var $this = $(this),
      label = $('#repeat-password-wrong');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight');
			} else {
		    label.removeClass('highlight');
			}
    } else if (e.type === 'focus') {

      if( $this.val() === '' ) {
    		label.removeClass('highlight');
			}
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {

  e.preventDefault();

  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');

  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();

  $(target).fadeIn(600);

});

// $('#signup-repeat-password').on('focusout', function() {
//     var password = $('#signup-password').val();
//     var repeat_password = $('#signup-repeat-password').val();
//
//     if (password != repeat_password) {
//         $('#repeat-password-wrong').show();
//         $('#repeat-password-correct').hide();
//     }
//     else {
//         $('#repeat-password-wrong').hide();
//         $('#repeat-password-correct').show();
//     }
// });

$('#signup-repeat-password').on('input', function() {
    var password = $('#signup-password').val();
    var repeat_password = $('#signup-repeat-password').val();

    if ( compare_passwords() ) { enable_submit_button() }
    else { disable_submit_button() }

    if (repeat_password.length >= password.length) {
        if (password != repeat_password) {
            $('#repeat-password-wrong').show();
            $('#repeat-password-correct').hide();
        }
        else {
            $('#repeat-password-wrong').hide();
            $('#repeat-password-correct').show();
        }
    }
});

$('#signup-password').on('input', function() {
    if ( compare_passwords() ) {
        enable_submit_button();
        $('#repeat-password-wrong').hide();
        $('#repeat-password-correct').show();
    }
    else {
        disable_submit_button();
        $('#repeat-password-wrong').show();
        $('#repeat-password-correct').hide();
    }
});

$('#signup-first-name, #signup-last-name, #signup-username, #signup-password').on('input', function() {
    if ($(this).val().length >= 4 ) {enable_submit_button()}
    else {disable_submit_button()}
});

function enable_submit_button(){
    if (validate_first_name() && validate_last_name() && validate_username() && validate_password() && compare_passwords()) {
        $('#submit-signup').prop('disabled', false);
    }
}

function compare_passwords(){
    var password = $('#signup-password').val();
    var repeat_password = $('#signup-repeat-password').val();

    return password == repeat_password;
}

function disable_submit_button(){
    $('#submit-signup').prop('disabled', true);
}

function validate_first_name(){
    var first_name = $('#signup-first-name').val();
    return first_name.length >= 4
}

function validate_last_name(){
    var last_name = $('#signup-last-name').val();
    return last_name.length >= 4
}

function validate_username(){
    var username = $('#signup-username').val();
    return username.length >= 4
}

function validate_password(){
    var password = $('#signup-password').val();
    return password.length >= 4
}

$('#login-username, #login-password').on('input', function() {
    if ($(this).val().length >= 4 ) {enable_login_submit_button()}
    else {disable_login_submit_button()}
});

function enable_login_submit_button(){
    if ($('#login-username').val().length >= 4 && $('#login-password').val().length >= 4) {
        $('#submit-login').prop('disabled', false);
    }
}

function disable_login_submit_button(){
    $('#submit-login').prop('disabled', true);
}
