/*##################################################|*/
/* #CMS.SETUP# */
(function namespacing() {
	// insuring django namespace is available when using on admin
	django = window.django || undefined;

	// assign global namespaces
	window.CMS = {
		'$': (django) ? django.jQuery : window.jQuery || undefined,
		'Class': Class.$noConflict(),
		'API': {}
	};
})();
