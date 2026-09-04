let games = {}

function create_game_block(data)
{
	let ribbon = ''
	if (data.ribbon == 'new')
	{
		ribbon = '<div class="ribbon_new font-display_top text-xl" style="z-index:2;">NEW</div>'
	}
	else if (data.ribbon == 'popular')
	{
		ribbon = '<div class="ribbon_popular font-display_top text-md" style="z-index:2;">POPULAR</div>'
	}
	return `
	<div class="relative overflow-hidden rounded-2.5xl bg-white dark:bg-jacarta-700">
		`+ribbon+`						
		<figure class="relative">
		<a
			href="/blogs/`+data.route_url_en+`"
			class="group block after:absolute after:inset-0 after:block after:bg-jacarta-900/20"
		>
			<img
			src="/cs/uploads/`+data.img+`"
			class="w-full object-cover transition-transform duration-[1600ms] will-change-transform group-hover:scale-105"
			loading="lazy"
			decoding="async"
			fetchpriority="low"
			alt="`+data.name+`"
			>
		</a>
		</figure>
		<div class="pointer-events-none absolute bottom-0 w-full p-5 " style="background: rgba(43,25,68, 0.6);">
		<h2 class="font-display text-base leading-none text-white xl:text-base" style="text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9),  0 0 10px rgba(0, 0, 0, 0.7); ">`+data.name+`</h2>
		</div>
	</div>
	`
}

function create_list_by_order(data)
{
	$('#get_catalog').empty()
	data.forEach(game => {
		$('#get_catalog').append(create_game_block(game))
	});		
}

$(document).ready(function() { 
	$.get('/games_catalog/get_catalog', function(dataout)
	{
		var data = JSON.parse(dataout)
		games = data
		for (const [key, value] of Object.entries(games)) {
			$('#art_'+key).replaceWith(create_game_block(value))
		}	
	});	
	$('#filter_block').removeClass('disabled_div')
});

$('#games_catalog').on('click', '.order_choose', function (event) {
	$('#search_cat').val('')
    let key = $(this).attr('data-key');
    let target = $('[data-key="' + key + '"]');
	let cleanText = target.text().replace(/\s+/g, ' ').trim();
    $('#order_choose').text(cleanText);
    $('.checked_order').remove();
    $('#' + key).html(target.text() + '<i class="fa fa-check text-accent checked_order"></i>');
    let gamesArray = Array.isArray(games) ? games : Object.values(games);

    if (key == 'alphabet') { 
		gamesArray.sort((a, b) => a.name.localeCompare(b.name)); 
		create_list_by_order(gamesArray);
	}
	else if (key == 'default') { 
		gamesArray.sort((a, b) => Number(a.order_by) - Number(b.order_by)); 
		create_list_by_order(gamesArray);
	}
	else if (key == 'date') { 
		let gamesArr = Object.keys(games).map(key => {
			return { key: Number(key), ...games[key] };
		});
		$('#get_catalog').empty()
		gamesArr.sort((a, b) => b.key - a.key);
		gamesArr.forEach(game => {
			$('#get_catalog').append(create_game_block(game))
		});			
	}		
});


	$('#search_cat').on('input', function () {
		let q = $(this).val().trim().toLowerCase();

		$('#get_catalog article').each(function () {
			var text = $(this).text().toLowerCase();
			var tags = ($(this).data('tags') || '').toLowerCase();
			if (q === '' || text.includes(q) || tags.includes(q)) {
				$(this).show();
			} else {
				$(this).hide();
			}
		});
	});