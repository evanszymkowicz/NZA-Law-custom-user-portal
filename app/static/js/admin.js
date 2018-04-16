//* Designing Popup error/notify messaging *//
window.onload = function () {
  var first_name_data = $('#my-data').data("fname");
  var last_name_data = $('#my-data').data("lname");
  var role_data = $('#my-data').data("role");
  var id_data = parseInt($('#my-data').data("u_id"));
  $("#first_name").attr("value", first_name_data);
  $("#last_name").attr("value", last_name_data);
  $('select option[value=' + role_data + ']').attr("selected",true);
  $("#user_id").attr("value", id_data);
  $("#user_id").prop("readonly", true);
  $("#delete").attr("value", "Type 'REMOVE'");
  $("#user_id_delete").attr("value", id_data);
  $("#user_id_delete").hide();
}
