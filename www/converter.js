function calculateFormulas() {
	var rate = document.getElementById("rate_input").value;
	$.get("https://gmkydyl926.execute-api.eu-west-1.amazonaws.com/V1/rate/" + rate, viewResult);
	//viewResult('{"formulas": [{"difficulty": 0, "rate": 0.1, "expression": "\frac{x}{10}", "error": 0.0}], "rate": 0.1}',200);
}
function viewResult(data, status){

// Create headers
$('#result').empty();
var $line = $( "<tr></tr>" );
$line.append( $( "<th></th>" ).html( "Error" ) );
$line.append( $( "<th></th>" ).html( "Rate" ) );
$line.append( $( "<th></th>" ).html( "Formula") );
$('#result').append( $line );

// Add results to table
for (i in data.formulas) {
    item = data.formulas[i];
    $line = $( "<tr></tr>" );
    $line.append( $( "<td></td>" ).html((Math.round(item.error*10000)/100 + "%" ) ));
    $line.append( $( "<td></td>" ).html( (Math.round(item.rate*1000)/1000 ) ) );
    $line.append( $( '<td aling="left"></td>' ).html( "$$" + item.expression + "$$") );
    $('#result').append( $line );
}
//$table.appendTo( document.getElementById('result') );

// Format formulas
MathJax.Hub.Typeset();
}

function addOptions(data, status) {
	rates = data.rates;
	rates.EUR = 1;
	$('#from').empty();
	for( currency in data.rates){
		rate = rates[currency];
		
		from_img = document.createElement("img");
		from_img.src = "flags/" + currency + ".png";
		from_img.width = "30";
		
		from_option = document.createElement("option");
		from_option.value = currency;
		from_option.append(from_img);
		from_option.append(" " + currency);
		
		if(currency === 'USD'){
			from_option.selected = "selected";
		}			
	
		$('#from').append(from_option);
		
		to_img = document.createElement("img");
		to_img.src = "flags/" + currency + ".png";
		to_img.width = "30";
		to_option = document.createElement("option");
		to_option.value = currency;
		//to_option.append(to_img);
		to_option.append(to_img);
		to_option.append(' ' + currency);
		
		if(currency === 'EUR'){
			to_option.selected = "selected";
		}
		
		$('#to').append(to_option);
	}
	getRate();
}

$(document).ready(function() {
  //$("#from").selectpicker('refresh');
  //$("#to").selectpicker('refresh');
});


function getRate(){
	from_cur = $('#from').val();
	to_cur = $('#to').val();
	from_rate = rates[from_cur];
    to_rate = rates[to_cur];
	if(from_rate){
		rate = Math.round(to_rate/from_rate*100000)/100000;
		document.getElementById("rate_input").value = rate;

		instructions = "You can convert <i>x</i> " + from_cur + " to " + to_cur + " with the following formulas. The first formulas are the most accurate ones, but might also be slightly difficult."
		document.getElementById("instructions").innerHTML = instructions;
				
		calculateFormulas();
	}
}
	
function swap(){
	from_cur = $('#from').val();
	to_cur = $('#to').val();
	
	$('#from').selectpicker('val', to_cur);
	$('#to').selectpicker('val', from_cur);
	
	getRate();
	$('.selectpicker').selectpicker({});
}

