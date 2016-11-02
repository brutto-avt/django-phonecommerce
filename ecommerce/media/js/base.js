$(function() {
	// slideshow
	$('#slider').tabs({show: {effect: "fade", duration: 800}}).tabs("rotate", 5000, true);

	//search
	$('#search input').click(function() {
		if ($(this).val() == 'buscar telefones') {
			$(this).val('');
		}
	});

	$('#search input').focusout(function() {
		if ($(this).val().length == 0) {
			$(this).val('buscar telefones');
		}
	});

	// throttling
	function throttle(fn, delay) {
  		var timer = null;
  		return function () {
    		var context = this, args = arguments;
    		clearTimeout(timer);
    		timer = setTimeout(function () {
      			fn.apply(context, args);
    		}, delay);
  		};
	}

	// live search
	$('#search input').keyup(throttle(function(e) {
		if (e.keyCode == 27) {
			$('#live-search').fadeOut();
			$('#search input').removeClass('active');
			$(this).val('buscar telefones');
		} else {
			var q = $.trim($(this).val());
			if (q.length > 0) {
				if (q.length == 1) {
					$('#live-search').fadeIn();
				} else {
					$.ajax({
						type: 'GET',
						cache: false,
						dataType: 'json',
						assync: false,
						url: $(this).parent().attr('action'),
						data: 'q='+q,
						success: function(data) {
							if ($(data).attr('html')) {
								$('#live-search').fadeIn();
								$('#live-search').html(data.html);
								$('#search input').addClass('active');
							}
							
						}
					});
				}
			} else {
				$('#live-search').fadeOut();
				$('#search input').removeClass('active');
				$(this).val('buscar telefones');
			}
		}
		return false;
	}, 300));

	// drag
	$('.drag').draggable({
		cursor: 'move',
		revert: true,
		revertDuration: 90,
		containment: 'document',
		start: function() {
			$('#cart-drop').addClass('open');
			$('#cart-drop').fadeIn();
		},
		stop: function() {
			$('#cart-drop').fadeOut();
		}
	});

	// drop
	$('#cart-drop').droppable({
		drop: function(event, ui) {
			$('#cart-drop').removeClass('open');
			$.fancybox.showLoading();
			$.ajax({
				type: 'POST',
				cache: false,
				dataType: 'json',
				assync: false,
				data: 'quantidade=1',
				url: ui.draggable.attr('rev'),
				success: function(data) {
					$.fancybox(data.msg);
					if ($(data).attr('n_itens')) {
						$('#cart-top a').text(data.n_itens + ' ITENS');
					}
					
				}
			});
		}
	});

	Number.prototype.formatMoney = function(c, d, t){
		var n = this, 
		c = isNaN(c = Math.abs(c)) ? 2 : c, 
		d = d == undefined ? "." : d, 
		t = t == undefined ? "," : t, 
		s = n < 0 ? "-" : "", 
		i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
		j = (j = i.length) > 3 ? j % 3 : 0;
	   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
	 };
	
	// data grid
	$.getJSON("/carrinho/config/", function(data){
		try {
			$("#carrinho-grid").jqGrid(data).navGrid('#pager', {
				add: false,
				edit: true,
				del: true,
				search: false,
				view: true,
			},
			{
				url:'/carrinho/edita/',
				closeAfterEdit: true,
				afterComplete: function(response, postdata, formid) {
					var json = $.parseJSON(response.responseText);
					$.fancybox(json.msg);
					try {
						$('p.total span').text('R$ '+json.total.formatMoney(2, ',', '.'));					
					} catch(e) {}
				}
			},
			{},
			{
				url: '/carrinho/remove/',
				afterComplete: function(response, postdata, formid) {
					var json = $.parseJSON(response.responseText);
					$.fancybox(json.msg);
					try {
						$('p.total span').text('R$ '+json.total.formatMoney(2, ',', '.'));					
					} catch(e) {}
				}
			});
		} catch(e) {}
	});

	// scroll panel
	$("#main #whats-hot, #main #deal-of-day").mCustomScrollbar({
		horizontalScroll:true,
		theme:'dark',
		advanced:{
			updateOnContentResize: true
		}
	});

	// tabbed widget
	$('#main .tabbed-widget').tabs();

	// footer form
	$('#footer form #name').click(function() {
		if ($(this).val() == 'Nome') {
			$(this).val('');
		}
	});

	$('#footer form #name').focusout(function() {
		if ($(this).val().length == 0) {
			$(this).val('Nome');
		}
	});

	$('#footer form #email').click(function() {
		if ($(this).val() == 'E-mail') {;
			$(this).val('');
		}
	});

	$('#footer form #email').focusout(function() {
		if ($(this).val().length == 0) {
			$(this).val('E-mail');
		}
	});

	// lightbox
	$('a.fancybox').each(function() {
		$(this).fancybox({
			'titlePosition': 'outside',
			'overlayColor': '#000',
			'overlayOpacity': 0.9
		});
	});

	var buildParams = function(form, onlyChecked) {
		output = ''
		nItems = 0;
		for (i=0; i<form.elements.length; i++) {
			add = true;
			if (form.elements[i].type != "text" && form.elements[i].type != "number" && onlyChecked && !form.elements[i].checked) {
				add = false;
			}
			if (add) {
				if (nItems > 0) {
					output += '&amp;'
				}
				output += form.elements[i].name + '=' + form.elements[i].value;
				nItems += 1;
			}
		}
		return output;
	};
	
	$('a.fancybox-ajax').each(function() {
		rev = $(this).attr('rev');
		$(this).fancybox({
			'titlePosition': 'outside',
			'overlayColor': '#000',
			'overlayOpacity': 0.9,
		});
		$(this).click(function(event) {
			form = document.forms[$(this).attr('rev')];
			params = buildParams(form, true);
			$.fancybox.showLoading();
			$.ajax({
				type: 'POST',
				cache: false,
				dataType: 'json',
				assync: false,
				url: $(this).attr('href'),
				data: params,
				success: function(data) {
					$.fancybox(data.msg);
					if ($(data).attr('n_itens')) {
						$('#cart-top a').fadeOut();
						$('#cart-top a').text(data.n_itens + ' ITENS');
						$('#cart-top a').fadeIn();
					}
					
				}
			});
			return false;
		});
	});

	// remove item
	$('a.fancybox-remove').each(function() {
		$(this).fancybox({
			'titlePosition': 'outside',
			'overlayColor': '#000',
			'overlayOpacity': 0.9,
		});
		$(this).click(function(event) {
			$.fancybox.showLoading();
			$.ajax({
				type: 'POST',
				cache: false,
				dataType: 'json',
				assync: false,
				url: $(this).attr('href'),
				success: function(data) {
					$.fancybox(data.msg);
					if ($(data).attr('n_itens')) {
						$('#cart-top a').text(data.n_itens + ' ITENS');
					}
					
				}
			});
			$(this).parent().parent().fadeOut();
			return false;
		});
	});

	//confirm order
	$('#confirm-order').click(function(event) {
		url = $(this).attr('href');
		$("#dialog").dialog({
			modal : true,
			closeOnEscape: false,
			dialogClass: 'noclose',
			resizable : false,
			width : 450,
			title : 'Deseja continuar?',
			buttons : {
				"Sim" : function() {
					$(this).dialog("close");
					$(location).attr('href', url);
				},
				"Não" : function() {
					$(this).dialog("close");
				}
			}
		});
		event.preventDefault();
	});
});