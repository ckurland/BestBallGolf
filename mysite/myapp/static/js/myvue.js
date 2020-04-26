
var instance_id = document.getElementById('tID').value;
var teamName = document.getElementById('teamName').value;
//player list
var app = new Vue({
    el: '#app',
    data: {
      availPlayers: [],
	  teams: [],
	  tName: teamName,
      seen:true,
      unseen:false,
      tseen:true,
      tunseen:false
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
          this.tseen=false
          this.tunseen=true
      },
		
      cancelAutoUpdate: function() { clearInterval(this.timer) }
    },
    beforeDestroy() {
      clearInterval(this.timer)
    }
  
  })

function addPlayer(playerID) {
	console.log("HTLELPDSFASF")
	const response = axios.get('/addPlayer/'+instance_id+'/'+playerID+'/');
	console.log(response);

}

