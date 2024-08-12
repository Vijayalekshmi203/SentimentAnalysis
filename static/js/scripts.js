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
