$(document).ready(function () {
	$('#castList li:lt(6)').show();
	$('#loadMore').click(function () {
		$('#castList li').show();
		$('#showLess').show();
		$('#loadMore').hide();
	});
	$('#showLess').click(function () {
		$('#castList li').not(':lt(6)').hide();
		$('#showLess').hide();
		$('#loadMore').show();
	});
});