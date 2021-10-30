function addToLocalStorage(key,data){
    localStorage.setItem(key) = data;
}

function retrieveFromLocalStorage(key){
    return localStorage.getItem(key)
}

function logout(){
    $.ajax({
        type: "POST",
        url: "/logout",
        success: function(data) {
            console.log(data)
            window.location.href = "login";
        }
    });
}

function history(e){
    const form = new FormData(e.target);
    date = form.get("date")
    console.log(date)
    $.ajax({
        type: "POST",
        url: "/ajaxhistory",
        data:{
            "date":date
        },
        success: function(response){
            console.log(response)
            resdata = JSON.parse(response)
            
            $("#date_legend").empty().append("Date: ")
            $("#date").empty().append(resdata.date)

            $("#calories_legend").empty().append("Calories: ")
            $("#calories").empty().append(resdata.calories)

            $("#burnout_legend").empty().append("Burnout: ")
            $("#burnout").empty().append(resdata.burnout)

            $("#history-data").empty().append(JSON.stringify(response));
        }
    })
}