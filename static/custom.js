	$(document).ready(function(){
		$("#deletestk").click(function(event){
			event.preventDefault();
			$.get("/stock/delete/"+$("#deleteStk #stockNameDel").val() +"/"+$("#deleteStk #stockPortDel").val(),function(data, status){
				$("#deleteStkMsg").prepend(data);
			});
		});
		$("#getstklist").click(function(event){
			event.preventDefault();
			$.get("/stock/allStocks",function(data, status){
				stockListOutput = '';
				results = eval('('+data+')');
				console.log(results);

				//for(var i = 0; i < results.length; i++) {
				//	console.log(data[i].ticker);
				//	stockListOutput += stockListOutput +'<br />';
				//}
				$.each(results,function(){
					stockListOutput += 'You recorded '+this.shares+' shares of '+this.ticker +' in "'+this.portfolio +'" portfolio.<br />';
					console.log(this);
					//alert(this.value);
					//alert(this.label);

					//var option = $("<option />");
					//option.attr("value", this.value).text(this.label);
				});
				$("#stkmsgarea").prepend(stockListOutput +"<hr>");
			});
		});
		$("#addstock").click(function(event){
			/* Stop form form submitting normally */
			event.preventDefault();
			$.post("/stock/addUpdate", $("#addStock").serialize(), function(response, status){
				//responseObj = eval('('+response+')');
				console.log("Response: "+response);
				$("#stkmsgarea").prepend(response+"<br /><hr>");
			});
		});
		
		$("#portInfoBtn").click(function(event){
			/* Stop form form submitting normally */
			event.preventDefault();
			$.get("/portfolio/portfolioDetails/"+ $("#portfolioInfoName").val(), function(response, status){
				//responseObj = eval('('+response+')');
				console.log("Response: "+response);
				$("#portInfoMessages").prepend(response+"<br /><hr>");
			});
		});
		
		
		$("#portfolioDeleteBtn").click(function(event){
			/* Stop form form submitting normally */
			event.preventDefault();
			$.get("/portfolio/portfolioDelete/"+ $("#portfolioDeleteName").val(), function(response, status){
				//responseObj = eval('('+response+')');
				console.log("Response: "+response);
				$("#portDeleteMessages").prepend(response+"<br /><hr>");
			});
		});
		
		$("#getportlist").click(function(event){
			event.preventDefault();
			$.get("/portfolio/fullList", function(data, status){
				$("#msgarea2").prepend(data+"<br /><hr>");
			});
		});
		$("#addportname").click(function(event){
			/* Stop form from submitting normally */
			event.preventDefault();
			$.post('/portfolio/', $("#addPort").serialize(), function(response, status){
				$("#msgarea2").prepend(response + "<br /><hr>");
			});
		});
	});