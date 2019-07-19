// This file is autogenerated. See modules.json and autogenerator.py for details

/*
	get_redirects.js

	MediaWiki API Demos
	Demo of `Redirects` module: Get all redirects to the given page(s)

	MIT License
*/

var params = {
		action: 'query',
		titles: 'Jacques Kallis',
		prop: 'redirects',
		format: 'json'
	},
	api = new mw.Api();

api.get( params ).done( function ( data ) {
	var pages = data.query.pages,
		p;

	function result( p ) {
		pages[ p ].redirects.forEach( function ( re ) {
			console.log( re.title + ' redirect to ' + pages[ p ].title );
		} );
	}
	for ( p in pages ) {
		result( p );
	}
} );
