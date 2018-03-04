var fda_api = "https://api.fda.gov/drug/label.json?"
var limit = 10

new Vue({
	el: "#app",
	data: {
		searchBy: '',
		brandName: '',
		itemsPerRow: 3,
		items: []
	},
	computed:{
		rowCount:function(){
			return Math.ceil(this.items.length / this.itemsPerRow);
		},
	},
	watch: {
		searchBy: function() {
			this.items = []
			this.getDrugs(this.items, this.searchBy)
		},
	},
	methods: {
		itemCountInRow:function(index) {
     		return this.items.slice((index - 1) * this.itemsPerRow, index * this.itemsPerRow)
    	},
		getDrugs: function(items, searchBy=null) {
			api_url = fda_api + "limit=" + limit
			
			if (searchBy != null) {
				api_url = api_url + "&search=openfda.generic_name:" + searchBy
				api_url = api_url + "+search=openfda.brand_name:" + searchBy
			}

			console.log(api_url)
			axios.get(api_url)
				.then(function(response){
					products = response.data.results
					console.log(products)
					for (var i = 0; i < products.length; i++) {
						var id = products[i].id
						var generic_name = products[i].openfda.generic_name
						var brand_name = products[i].openfda.brand_name
						var product_type = products[i].openfda.product_type
						var route = products[i].openfda.route
						var purpose = products[i].purpose
						var indications_and_usage = products[i].indications_and_usage
						var warnings = products[i].warnings
						var active_ingredients = products[i].active_ingredients
						var inactive_ingredients = products[i].inactive_ingredients
						var storage_and_handling = products[i].storage_and_handling
						
						items.push({
							id: id,
							generic_name: generic_name,
							brand_name: brand_name,
							product_type: product_type,
							route: route,
							purpose: purpose,
							indications_and_usage: inications_and_usage,
							warnings: warnings,
							active_ingredients: active_ingredients,
							inactive_ingredients: indications_and_usage,
							storage_and_handling: storage_and_handling
						})
					}
				})
				.catch(function(error) {
					console.log("An error occured")
				})
		},
	},
	beforeMount() {
		this.getDrugs(this.items)
	}
})