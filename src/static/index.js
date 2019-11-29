// index.js
// 페이지 내에서 구현할 기능을 저장한 Javascript 파일

// 검색 문항을 받아 백엔드로 검색 쿼리 전달 및 결과 작성을 수행할 함수
function search() {
  var keyword = $("#search-input").val();
  var url = "/api/users/?name=" + keyword;
  curPage = 0;

  $.ajax(url)
    .done(function(result) {
      // 쿼리가 비어있지 않았다면 일치하는 갯수와 성이 같은 사람의 수를 출력
      $("#query-result-placeholder").prop("hidden", true);
      if (keyword != "") $("#query-result-placeholder").prop("hidden", false);
      $("#query-result-number").html(result.number);
      $("#first-name").html(result.first_name);
      $("#first-name-number").html(result.first_name_number);

      // 검색 결과가 없을 시 table과 pagination 제거
      if (result.number == 0) {
        $("#table-head").prop("hidden", true);
        $("#table-body").html("");
        $("#page-navigator").prop("hidden", true);
      }

      // 검색 결과가 있을 시 이를 이용하여 table 및 pagination 생성
      else {
        $("#table-head").prop("hidden", false);
        var str = "";
        for (var i = 0; i < result.user_list.length; i++) {
          str += '<tr class="tr-user" id="user-' + (i + 1) + '">';
          str +=
            '<td class="tr-user-uid" hidden>' +
            result.user_list[i]["id"] +
            "</td>";
          str += '<th class="tr-user-index" scope="row">' + (i + 1) + "</th>";
          str +=
            "<td class='tr-user-name'>" + result.user_list[i]["name"] + "</td>";
          str +=
            "<td class='tr-user-phone'>" +
            result.user_list[i]["phone"] +
            "</td>";
          str += `<td><div class="btn-group" role="group" aria-label="Action buttons">
                      <button type="button" class="btn btn-warning btn-update">수정</button>
                      <button type="button" class="btn btn-danger btn-delete">삭제</button>
                    </div></td>`;
          str += "</tr>";
        }
        $("#table-body").html(str);

        $("#page-navigator").prop("hidden", false);
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
      }
    })
    .fail(function(xhr) {
      console.log("error:" + xhr);
    });
}

// 페이지 로딩 완료 시 전체 연락처 출력
$(document).ready(function() {
  $("#search-input").val("");
  search();
});

// 검색 버튼이 눌러질 시 검색 시행
$("#search-button").click(function(event) {
  // 버튼에 할당된 기본 submit event 취소
  event.preventDefault();
  search();
});

// 페이지 이동 함수
$(".page-item").click(function() {
  console.log($(this).html);
  if ($(this).html() == "이전") {
  }
});

// 연락처 추가 클릭 시 연락처 추가 팝업 표시
$("#nav-user-add").click(function(event) {
  event.preventDefault();
  $("#modal-user-create").modal("show");
});

// 연락처 추가 팝업에서 전송을 눌렀을 경우
$("#user-create-form").submit(function(event) {
  event.preventDefault();

  $("#user-create-button").prop("disabled", true);
  $("#user-create-button").html(`
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    <span class="sr-only">처리중</span>
  `);

  // 연락처 추가 팝업 내 form에 있던 데이터를 이용하여
  // /api/users/ 에 JSON을 POST Request로 전송한다.
  var response = $.ajax("/api/users/", {
    method: "POST",
    data: JSON.stringify({
      name: $("#user-create-form-name").val(),
      phone: $("#user-create-form-phone").val()
    })
  });

  $("#user-create-button").prop("disabled", false);
  $("#user-create-button").html("추가");

  response.always(function(data) {
    if (data.status === 422) {
      console.log(data.responseJSON);
    } else {
      $("#user-create-form-name").val("");
      $("#user-create-form-phone").val("");
      $("#modal-user-create").modal("hide");
      $("#alert-placeholder").html(`
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          연락처 등록에 성공했습니다.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      `);
      search();
    }
  });
});

// 연락처 수정 클릭 시 연락처 추가 팝업 표시
$(document).on("click", ".btn-update", function() {
  $("#user-update-form-uid").val(
    $(this)
      .parent()
      .parent()
      .parent()
      .children(".tr-user-uid")
      .text()
  );
  $("#user-update-form-name").val(
    $(this)
      .parent()
      .parent()
      .parent()
      .children(".tr-user-name")
      .text()
  );
  $("#user-update-form-phone").val(
    $(this)
      .parent()
      .parent()
      .parent()
      .children(".tr-user-phone")
      .text()
  );
  $("#modal-user-update").modal("show");
});

// 연락처 수정 팝업에서 전송을 눌렀을 경우
$("#user-update-form").submit(function(event) {
  event.preventDefault();

  $("#user-update-button").prop("disabled", true);
  $("#user-update-button").html(`
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    <span class="sr-only">처리중</span>
  `);

  // 연락처 수정 팝업 내 form에 있던 데이터를 이용하여
  // /api/users/(사용자 id) 에 JSON을 PUT Request로 전송한다.
  var url = "/api/users/" + $("#user-update-form-uid").val();
  var response = $.ajax(url, {
    method: "PUT",
    data: JSON.stringify({
      name: $("#user-update-form-name").val(),
      phone: $("#user-update-form-phone").val()
    })
  });

  $("#user-update-button").prop("disabled", false);
  $("#user-update-button").html("수정");

  response.always(function(data) {
    if (data.status === 422 || data.status === 405) {
      console.log(data.responseJSON);
    } else {
      $("#user-update-form-uid").val("");
      $("#user-update-form-name").val("");
      $("#user-update-form-phone").val("");
      $("#modal-user-update").modal("hide");
      $("#alert-placeholder").html(`
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          연락처 수정에 성공했습니다.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      `);
      search();
    }
  });
});

// 연락처 삭제 클릭 시 연락처 추가 팝업 표시
$(document).on("click", ".btn-delete", function() {
  $("#user-delete-form-uid").val(
    $(this)
      .parent()
      .parent()
      .parent()
      .children(".tr-user-uid")
      .text()
  );
  $("#modal-user-delete").modal("show");
});

// 연락처 삭제 팝업에서 전송을 눌렀을 경우
$("#user-delete-form").submit(function(event) {
  event.preventDefault();

  $("#user-delete-button").prop("disabled", true);
  $("#user-delete-button").html(`
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    <span class="sr-only">처리중</span>
  `);

  // 연락처 추가 팝업 내 form에 있던 사용자 id를 이용하여
  // /api/users/(사용자 id) 로 DELETE Request로 전송한다.
  var url = "/api/users/" + $("#user-delete-form-uid").val();
  var response = $.ajax(url, {
    method: "DELETE"
  });

  $("#user-delete-button").prop("disabled", false);
  $("#user-delete-button").html("삭제");

  response.always(function(data) {
    if (data.status === 422 || data.status === 405) {
      console.log(data.responseJSON);
    } else {
      $("#modal-user-delete-uid").val("");
      $("#modal-user-delete").modal("hide");
      $("#alert-placeholder").html(`
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          연락처 삭제에 성공했습니다.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      `);
      search();
    }
  });
});
