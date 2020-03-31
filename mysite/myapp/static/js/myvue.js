
var instance_id = document.getElementById('lID').value;
//player list
var app = new Vue({
    el: '#app',
    data: {
      availPlayers: [],
	  teams: [],
      seen:true,
      unseen:false
    },
    //Adapted from https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
    created: function() {
          this.fetchPlayerList();
          this.fetchTeamList();
          this.timer = setInterval(this.fetchPlayerList, 10000);
    },
    methods: {
      fetchPlayerList: function() {
          axios
            .get('/availPlayers/'+instance_id+'/')
            .then(response => (this.availPlayers = response.data.availPlayers))
          console.log(this.availPlayers)
          this.fetchTeamList();
          this.seen=false
          this.unseen=true
      },
      fetchTeamList: function() {
          axios
            .get('/teamDraft/'+instance_id+'/')
            .then(response => (this.teams = response.data.teams))
          console.log(this.teams)
          this.seen=false
          this.unseen=true
      },
      cancelAutoUpdate: function() { clearInterval(this.timer) }
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  
  })

