var fda_api = "https://api.fda.gov/drug/label.json?"
var limit = 30

new Vue({
	el: "#app",
	data: {
		loading: false,
		search_by: this.search_by,
		filter_by: this.filter_by,
		error_msg: '',
		items_per_row: 3,
		page: 0,
		total_limit: 0,
		items: []
	},
	created () {
		this.getDrugs()
	},
	computed:{
		rowCount:function(){
			return Math.ceil(this.items.length / this.items_per_row);
		},
	},
	watch: {
		search_by: function() {
			this.items = []
			this.total_limit = 0
			this.page = 0
			this.getDrugs(this.items, this.search_by, this.filter_by)
		},
		filter_by: function() {
			this.items = []
			this.total_limit = 0
			this.page = 0
			this.getDrugs(this.items, this.search_by, this.filter_by)
		},
	},
	methods: {
		itemCountInRow: function(index) {
     		return this.items.slice((index - 1) * this.items_per_row, index * this.items_per_row)
    	},
		getDrugs: function() {

			var search_query = null
			var filter_query = null
			this.loading = true
			
			console.log("search_by:" + this.search_by)
			console.log("filter_by:" + this.filter_by)
			console.log("loading:" + this.loading)

			if (this.search_by == '') {
				this.search_by = null
			}

			api_url = fda_api + "limit=" + limit + "&skip="  + this.page + "&search="

			if (this.search_by != null) {
				search_query = "openfda.generic_name:" + this.search_by + "+openfda.brand_name:" + this.search_by
			}

			if (this.filter_by != null) {
				filter_query = "openfda.route:" + this.filter_by
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
//						var route = products[i].openfda.route
//						var purpose = products[i].purpose
//						var indications_and_usage = products[i].indications_and_usage
//						var warnings = products[i].warnings
//						var active_ingredients = products[i].active_ingredients
//						var inactive_ingredients = products[i].inactive_ingredients
//						var storage_and_handling = products[i].storage_and_handling
						
						this.items.push({
							id: id,
							generic_name: generic_name,
							brand_name: brand_name,
							product_type: product_type,
//							route: route,
//							purpose: purpose,
//							indications_and_usage: indications_and_usage,
//							warnings: warnings,
//							active_ingredients: active_ingredients,
//							inactive_ingredients: indications_and_usage,
//							storage_and_handling: storage_and_handling
						})
					}

//					this.loading = false
					setTimeout(this.loading = false, 10000);
					console.log("after loading: " + this.loading)

                    this.total_limit = this.total_limit + limit
                    console.log("loop", this.total_limit)

                    this.page = this.total_limit + 1
                    console.log("page", this.page)

                    setTimeout(function () { this.getDrugs() }.bind(this), 1000)

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
	}
})