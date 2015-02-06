$(document).ready(function(){
	var i = 0;

	var recognition = new webkitSpeechRecognition();
	recognition.continuous = true;

	//recognition.interimResults = true;

	recognition.onresult = function(event) { 
		console.log(event.results)
		var res = event.results[i][0].transcript;

		// Get sentiment of phrase.
		var params = {
		text: res,
		apikey: 'your_key',
		outputMode: 'json'
		}

		var url = 'http://access.alchemyapi.com/calls/text/TextGetTextSentiment';
		$.getJSON(url, params, function(data) {
			console.log(data);
			$('body').append(res+' ('+data.docSentiment.type+':'+data.docSentiment.score+')<br>');
			
			switch(data.docSentiment.type){
				case 'positive':
					var r = 10;
					var g = Math.round(parseFloat(data.docSentiment.score) * 255);
					var b = 10;
					$('body').css({background: 'rgba('+r+','+g+','+b+',.2)'});
					break;
				case 'negative':
					var g = 10;
					var r = Math.round(parseFloat(-data.docSentiment.score) * 255);
					var b = 10;
					$('body').css({background: 'rgba('+r+','+g+','+b+',.2)'});
					break;				
				default:
					var r = 10;
					var g = 10;
					var b = 10;
					$('body').css({background: 'rgba('+r+','+g+','+b+',.2)'});
					break;				
				}
		});

		i++;
	}
	recognition.start();      
});