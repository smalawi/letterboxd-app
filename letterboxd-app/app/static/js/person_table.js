// Table filter jQuery from https://www.mikestreety.co.uk/blog/filtering-tables/

var filterTable = function(item) {
	// Get the value of the select box
	var val = item.find(':selected').attr('filter-val');
	// Show all the rows
	$('tbody tr').show();
	// If there is a value hide all the rows except the ones with a data-year of that value
	if(val) {
		$('tbody tr').not($('tbody tr[data-role="' + val + '"]')).hide();
	}
}

$('#personSelect').on('change', function(e){
	filterTable($(this))
});

filterTable($('#personSelect'));