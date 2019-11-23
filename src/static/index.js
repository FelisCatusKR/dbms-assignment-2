var curPage = 0;

$("#search-button").click(function(event) {
  event.preventDefault();
  var words = $("#search-input").val();
  var url = "/api/users/";
  curPage = 0;
  url += "?name=" + words;
  if (words != "") {
    $.ajax(url)
      .done(function(result) {
        if (result.number > 0) {
          var thead = `<tr>
                        <th scope="col" class="sr-only">UID</th>
                        <th scope="col">#</th>
                        <th scope="col">이름</th>
                        <th scope="col">전화번호</th>
                        <th scope="col"><span class="sr-only">수정/삭제</span></th>
                      </tr>`;
          $("#table-head").html(thead);

          var str = "";
          for (var i = 0; i < result.user_list.length; i++) {
            str += '<tr id="user-' + (i + 1) + '">';
            str +=
              '<td class="user-id sr-only">' +
              result.user_list[i]["id"] +
              "</td>";
            str += '<th scope="row">' + (i + 1) + "</th>";
            str += "<td>" + result.user_list[i]["name"] + "</td>";
            str += "<td>" + result.user_list[i]["phone_number"] + "</td>";
            str += `<td><div class="btn-group" role="group" aria-label="Action buttons">
                      <button type="button" class="btn btn-warning">수정</button>
                      <button type="button" class="btn btn-danger">삭제</button>
                    </div></td>`;
            str += "</tr>";
          }
          $("#results").html(str);

          var page = "";
          page +=
            '<li class="page-item disabled"><a class="page-link" href="#" tabindex="-1" aria-disabled="true">이전</a></li>';
          page +=
            '<li class="page-item active" aria-current="page"><a class="page-link" href="#">1</a></li>';
          var leftPage = result.number - 100;
          for (var i = 2; leftPage > 0 && i <= 10; i++) {
            page +=
              '<li class="page-item"><a class="page-link" href="#">' +
              i +
              "</a></li>";
            leftPage -= 100;
          }
          if (leftPage)
            page +=
              '<li class="page-item"><a class="page-link" href="#">다음</a></li>';
          else
            page +=
              '<li class="page-item disabled"><a class="page-link" href="#" tabindex="-1" aria-disabled="true">다음</a></li>';
          $("#page-navigator").html(page);
        } else {
          $("#table-head").html("");
          $("#results").html("");
          $("#page-navigator").html("");
        }
      })
      .fail(function(xhr) {
        console.log("error:" + xhr);
      });
  } else {
    $("#table-head").html("");
    $("#results").html("");
    $("#page-navigator").html("");
  }
});
