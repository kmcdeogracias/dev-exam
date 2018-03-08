<template>
  <v-app>
    <h3 class="display-3">{{ msg }}</h3>
    <span class="subheading">U.S. Department of Health and Human ServicesFood and Drug Administration</span>
      <v-container grid-list-lg>
        <v-layout row align-center>
        <v-form v-model="valid">
        <v-text-field
          label="Search for generic or brand name"
          v-model="searchBy"
        ></v-text-field>
        </v-form>
        <v-select
          :items="filters"
          v-model="filterBy"
          label="Filter by route"
        ></v-select>
        </v-layout>
        <v-layout row v-for="i in rowCount">
          <v-flex xs4 v-for="item in itemCountInRow(i)">
            <v-card class="blue lighten-5" height="100%" hover>
              <v-card-title primary-title>
                <div>
                  <h3 class="mx-auto">{{ item.genericName }}</h3>
                </div>
              </v-card-title primary-title>
              <v-card-text>
                <p class="text-sm-left">Brand Name: {{ item.brandName }}</p>
                <p class="text-sm-left">Product Type: {{ item.productType }}</p>
              </v-card-text>
              <v-btn color="primary" @click.native.stop="dialog = true">Details</v-btn>
              <v-dialog v-model="dialog" max-width="350" @keydown.esc="dialog = false" fullscreen>
                <v-card>
                  <v-card-text>
                    <p class="text-sm-left">Route of Administration: {{ item.route }}</p>
                    <p class="text-sm-left">Purpose: {{ item.purpose }}</p>
                    <p class="text-sm-left">Indications and Usage: {{ item.indicationsAndUsage }}</p>
                    <p class="text-sm-left">Warnings: {{ item.warnings }}</p>
                    <p class="text-sm-left">Active Ingredients: {{ item.activeIngredients }}</p>
                    <p class="text-sm-left">Inactive Ingredients: {{ item.inactiveIngredients }}</p>
                    <p class="text-sm-left">Storage and Handling: {{ item.storageAndHandling }}</p>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </v-card>
          </v-flex>
        </v-layout>
        <v-progress-circular indeterminate :size="70" :width="7" color="indigo " v-show="loading"></v-progress-circular>
      </v-container>
  </v-app>
</template>

<script>
var fdaApi = 'https://api.fda.gov/drug/label.json?'
var limit = 10

console.log(limit)
export default {
  name: 'OpenFda',
  data () {
    return {
      msg: 'U.S FOOD AND DRUG ADMINISTRATION',
      loading: false,
      searchBy: this.searchBy,
		  filterBy: this.filterBy,
		  errorMsg: '',
		  itemsPerRow: 3,
		  page: 0,
		  totalLimit: 0,
		  items: [],
		  dialog: false,
		  filters: ['Oral', 'Topical', 'Intravenous', 'Dental', 'Respiratory', 'Opthalmic', 'Intramuscular', 'Subcutaneous', 'Nasal', 'Rectal']
    }
  },
  created () {
		this.getDrugs()
	},
	computed:{
		rowCount:function(){
			return Math.ceil(this.items.length / this.itemsPerRow);
		},
	},
	watch: {
		searchBy: function() {
			this.items = []
			this.totalLimit = 0
			this.page = 0
			this.getDrugs(this.items, this.searchBy, this.filterBy)
		},
		filterBy: function() {
			this.items = []
			this.totalLimit= 0
			this.page = 0
			this.getDrugs(this.items, this.searchBy, this.filterBy)
		},
	},
	methods: {
	  itemCountInRow: function(index) {
	    return this.items.slice((index - 1) * this.itemsPerRow, index * this.itemsPerRow)
	  },
	  getDrugs: function() {
	    console.log(this.items)
	    var searchQuery = null
	    var filterQuery = null
	    this.loading = true

	    console.log("searchQuery", searchQuery)
	    console.log("filterQuery", filterQuery)
	    console.log("loading", this.loading)

	    if (this.searchBy == '') {
	      this.searchBy = null
			}

			var apiUrl = fdaApi+ "limit=" + limit + "&skip="  + this.page + "&search="

			if (this.searchBy != null) {
			  searchQuery = "openfda.generic_name:" + this.searchBy + "+openfda.brand_name:" + this.searchBy
			}

			if (this.filterBy != null) {
			  filterQuery = "openfda.route:" + this.filterBy
			}

			if (searchQuery != null && filterQuery != null) {
				apiUrl = apiUrl + searchQuery + "+AND+" + filterQuery
			} else if (searchQuery != null) {
				apiUrl = apiUrl + searchQuery
			} else if (filterQuery != null) {
				apiUrl = apiUrl + filterQuery
			}

			console.log(apiUrl)

			axios.get(apiUrl)
			  .then(function(response) {
			    var products = response.data.results
					for (var i = 0; i < products.length; i++) {
            if (Object.keys(products[i].openfda).length > 0) {

              var id = products[i].id
              var genericName = products[i].openfda.generic_name[0]
              var brandName = products[i].openfda.brand_name[0]
              var productType = products[i].openfda.product_type[0]
              var route = products[i].openfda.route[0]
              var purpose = products[i].purpose
              var indicationsAndUsage = products[i].indications_and_usage
              var warnings = products[i].warnings
              var activeIngredients = products[i].active_ingredient
              var inactiveIngredients = products[i].inactive_ingredient
              var storageAndHandling = products[i].storage_and_handling

              console.log(id)
              this.items.push({
                id: id,
                genericName: genericName,
                brandName: brandName,
                productType: productType,
                route: route,
                purpose: purpose,
                indicationsAndUsage: indicationsAndUsage,
                warnings: warnings,
                activeIngredients: activeIngredients,
                inactiveIngredients: inactiveIngredients,
                storageAndHandling: storageAndHandling
              })
            }
          }

          setTimeout(this.loading = false, 10000);
					console.log("after loading: " + this.loading)

          this.totalLimit = this.totalLimit + limit
          this.page = this.totalLimit + 1

          console.log("loop", this.totalLimit)
          console.log("page", this.page)

          setTimeout(function () { this.getDrugs() }.bind(this), 1000)
			  }.bind(this), 1000)
			  .catch(function(error) {
			    console.log(error)
			    var status = error.response.status
			    if (status == 400) {
			      this.errorMsg = "No more products to display"
			    }
			    this.loading = false
			    console.log("An error occurred")
			  }.bind(this), 1000)
	  }
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
