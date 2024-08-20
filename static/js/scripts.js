jQuery('.confirm_leave').confirm({
	theme: 'supervan',
	icon: 'fa fa-spinner fa-spin',
	columnClass: 'col-md-6 col-md-offset-3',
	autoClose: 'Cancel|8000',
	title: 'Are you sure?',
	content: 'You are now leaving My Prediction Website',
	buttons: {
		Continue: function () {
			window.open(this.$target.attr('href'));
		},
		Cancel: function () {
			$.alert('Thank you for staying back');
		}
	}
});

// $(document).bind("contextmenu",function(e) {
// 	e.preventDefault();
// });
// $(document).keydown(function(e){
// 	if(e.which === 123){
// 		return false;
// 	}
// 	if (e.ctrlKey && e.shiftKey && (e.keyCode == 'I'.charCodeAt(0) || e.keyCode == 'i'.charCodeAt(0))) {
// 		return false;
// 	}
// });

AOS.init();

$(document).ready(function() {
	$('.opening_slider_wrap').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		dots: false,
		arrows: false,
		autoplay: true,
		autoplaySpeed: 2000,
		infinite: true,
		speed: 1000,
		rows: 0,
		adaptiveHeight: true
	});
	$('#copy_year').text(new Date().getFullYear());
});

$(window).scroll(function() {
	if ($(this).scrollTop() > 50 ) {
		$('.scrolltop:hidden').stop(true, true).fadeIn();
	} else {
		$('.scrolltop').stop(true, true).fadeOut();
	}
	$(window).trigger('resize');
	AOS.refresh();
});
$(function(){
	$(".scroll").click(function(){
		$("html,body").animate({scrollTop:$("body").offset().top},"1000");
		return false;
	});
});

$(window).on('load', function () {
	AOS.refresh();
});



document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('result_container').innerHTML = data;
        document.getElementById('result_sec').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});

// To find the word count of the text input in the form
function countWords() {
    const textarea = document.getElementById('translate_txt');
    const wordCountDisplay = document.getElementById('word_count');
    const submitButton = document.getElementById('submit_btn');
    
    const words = textarea.value.trim().split(/\s+/).filter(word => word.length > 0);
    const wordCount = words.length;

    wordCountDisplay.textContent = `${wordCount} / 500 words`;

    if (wordCount > 500) {
        wordCountDisplay.style.color = 'red';
        submitButton.disabled = true;
    } else {
        wordCountDisplay.style.color = 'black';
        submitButton.disabled = false;
    }
}

//To clear the form
function clearForm() {
	// Clear the file input
	document.getElementById('file_input').value = '';
	
	// Clear the text area
	document.getElementById('translate_txt').value = '';
}

