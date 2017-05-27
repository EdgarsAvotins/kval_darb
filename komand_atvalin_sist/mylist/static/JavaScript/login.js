// sākumā paslēpt ziņu "nesakrīt paroles" un atspējot pogas, kamēr nav aizpildīti lauki
$(function(){
    $('#repeat-password-wrong').hide();
    $('#submit-signup').prop('disabled', true);
    $('#submit-login').prop('disabled', true);
});

// ja ir pieslēgšanās kļūdas ziņojums, tad pāriet uz pieslēgšanās sadaļu
$(document).ready(function (){
    if ($('#login-error-message').text().length) {$('#login-tab').click();}
});

// rakstot un spaidot ievades logus, placeholder kustās vai maina krāsu. šeit tikai maina klasi, pārējo izpilda login.css
// sāk rakstīt - active highlight
// beidz rakstīt - highlight
// tukšs logs un neraksta - nav klases, abas noņemtas
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

// šis attiecas tikai uz ziņu "paroles nesakrīt", tā kā tā sākumā nav redzama un strādā nedaudz citādāk
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

// ja uzspiež citu sadaļu (reģistrēties/pieslēgties), tad nomaina klasi priekš krāsas, paslēpj vienu formu, parāda otru
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

// ja "atkārtot paroli" ir tikpat simbolu vai vairāk, tad salīdzināt
// ja nesakrīt paroles, tad nomainīt placeholder "parole" uz "password
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

// ja kaut ko ievada logā "parole" un kaut kas jau ierakstīts logā "atkārtot paroli"
// tad salīdzināt. un ja nav vienādas, tad parādīt placeholderi "paroles nesakrīt"
$('#signup-password').on('input', function() {
    if ($('#signup-repeat-password').val().length > 0) {
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
    }
});

// ja ievada vārdu, uzvārdu, lietotājvārdu vai paroli
// un ja ir jau ievadīti 4 vai vairāk simboli
// tad mēģināt aktivizēt "reģistrēties" pogu, bet vispirms tā metode pārbauda arī, vai tiešām viss kārtībā
$('#signup-first-name, #signup-last-name, #signup-username, #signup-password').on('input', function() {
    if ($(this).val().length >= 4 ) {enable_submit_button()}
    else {disable_submit_button()}
});

// ja pilnīgi viss ir kārtībā, tad aktivizēt "reģistrēties" pogu
function enable_submit_button(){
    if (validate_first_name() && validate_last_name() && validate_username() && validate_password() && compare_passwords()) {
        $('#submit-signup').prop('disabled', false);
    }
}

// salīdzina paroles, atgriež rezultātu
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

// ja ir 4 vai vairāk simbolu, mēģināt aktivizēt "pieslēgties" pogu
$('#login-username, #login-password').on('input', function() {
    if ($(this).val().length >= 4 ) {enable_login_submit_button()}
    else {disable_login_submit_button()}
});

// ja viss kārtībā, tad aktivizēt pogu
function enable_login_submit_button(){
    if ($('#login-username').val().length >= 4 && $('#login-password').val().length >= 4) {
        $('#submit-login').prop('disabled', false);
    }
}

function disable_login_submit_button(){
    $('#submit-login').prop('disabled', true);
}
