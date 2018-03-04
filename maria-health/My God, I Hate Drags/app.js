new Vue({
  el: '#app',
  data: {
    itemsPerRow: 4,
    items: [
    	{
    		generic_name: "melai"
    	},
    	{
    		generic_name: "ds"
    	},
    	{
    		generic_name: "meelai"
    	},
    	{
    		generic_name: "melfewai"
    	}

    ]
  },
  computed:{
    rowCount:function(){
      return Math.ceil(this.items.length / this.itemsPerRow);
    },
  },
  methods:{
    itemCountInRow:function(index){
     return this.items.slice((index - 1) * this.itemsPerRow, index * this.itemsPerRow)
    },
    setName () {
    	len = this.itemsPerRow;
    	for (var i = 0; i < len; i++) {
    		console.log(this.items[i].generic_name)
    	}
    		// this.items[0].generic_name = "Kim"
    }
  },
  beforeMount() {
  	this.setName()
  }
})