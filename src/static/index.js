var json = null;

$("#search-button").click(function(event) {
  event.preventDefault();
  var words = $("#search-input").val();
  var url = "/api/users/";
  url += "?name=" + words;
  if (words != "") {
    $.ajax(url)
      .done(function(result) {
        if (result.number > 0) {
          json = result;
          var str = "";
          for (var i = 0; i < result.user_list.length; i++) {
            str += "<tr>";
            str += '<th scope="row">' + (i + 1) + "</th>";
            str += "<td>" + result.user_list[i]["name"] + "</td>";
            str += "<td>" + result.user_list[i]["phone_number"] + "</td>";
            str += "</tr>";
          }
          $("#results").html(str);
        } else {
          $("#results").html("");
        }
      })
      .fail(function(xhr) {
        console.log("error:" + xhr);
      });
  } else {
    $("#results").html("");
  }
});
