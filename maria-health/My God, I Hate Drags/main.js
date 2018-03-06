var fda_api = "https://api.fda.gov/drug/label.json?"
var limit = 20

new Vue({
	el: "#app",
	data: {
		loading: false,
		search_by: this.search_by,
		filter_by: this.filter_by,
		error_msg: '',
		items_per_row: 3,
		items: []
	},
	created () {
		this.getDrugs(this.items)
	},
	computed:{
		rowCount:function(){
			return Math.ceil(this.items.length / this.items_per_row);
		},
	},
	watch: {
		search_by: function() {
			this.items = []
			this.getDrugs(this.items, this.search_by, this.filter_by)
		},
		filter_by: function() {
			this.items = []
			this.getDrugs(this.items, this.search_by, this.filter_by)
		},
	},
	methods: {
		itemCountInRow:function(index) {
     		return this.items.slice((index - 1) * this.items_per_row, index * this.items_per_row)
    	},
		getDrugs: function(items, search_by=null, filter_by=null) {
			
			var search_query = null
			var filter_query = null
			this.loading = true
			
			console.log("search_by:" + search_by)
			console.log("filter_by:" + filter_by)
			console.log("loading:" + this.loading)

			if (search_by == '') {
				search_by = null
			}

			api_url = fda_api + "limit=" + limit + "&search="

			if (search_by != null) {
				search_query = "openfda.generic_name:" + search_by + "+openfda.brand_name:" + search_by
			}

			if (filter_by != null) {
				filter_query = "openfda.route:" + filter_by
			}

			if (search_query != null && filter_query != null) {
				api_url = api_url + search_query + "+AND+" + filter_query 
			} else if (search_query != null) {
				api_url = api_url + search_query
			} else if (filter_query != null) {
				api_url = api_url + filter_query
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
							indications_and_usage: indications_and_usage,
							warnings: warnings,
							active_ingredients: active_ingredients,
							inactive_ingredients: indications_and_usage,
							storage_and_handling: storage_and_handling
						})
					}

					this.loading = false
					console.log("after loading: " + this.loading)
				}.bind(this),1000)
				.catch(function(error) {
					status = error.response.status
					if (status == 404) {
						this.error_msg = "No more products to display"
					}
					this.loading = false
					console.log("An error occured")
				}.bind(this), 1000)
		},
	},
})