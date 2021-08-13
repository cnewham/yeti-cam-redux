function updateStatus(name) {
  $.ajax({
    type: "GET",
    url: "api/v1/status/" + name,
    dataType: "json",
    error: function (error) {
      if (error.status != 404) {
        showAlert("An error occurred: " + error.status + " " + error.statusText, color=alerts.red);
      }
    },
    success: function (result) {
      status = "<table style='width:100%'>";
      $.each(result, function (key, value) {
        status += "<tr><td>" + key + "</td><td>" + value + "</td></tr>";
      });
      status += "</table>";

      elem = $("#" + name + " .status")
      elem.html(status);
    }
  });
}

function updateImage(name) {
  current = Flask.url_for("captures", {"name":name,"filename": "current.jpg"});

  newImage = $("#" + name + " .capture");
  newImage.attr("src", current + "?" + new Date().getTime());
}

function toggleOnlineStatus(cam) {
  if (cam.connected) {
    $("#" + cam.name + " .online").prop("hidden", false);
    $("#" + cam.name + " .offline").prop("hidden", true);
  } else {
    $("#" + cam.name + " .online").prop("hidden", true);
    $("#" + cam.name + " .offline").prop("hidden", false);
  }
}

function init() {
  $.ajax({
        type: "GET",
        url: "api/v1/capture",
        dataType: "json",
        error: function (error) {
          showAlert("An error occurred: " + error.status + " " + error.statusText, color=alerts.red);
        },
        success: function (result) {

          var cams = [];

          $.each(result, function(idx, data) {
            if (!data["hidden"]) {
                cams.push(data);
            }
          });

          cams.sort(function (a,b) { return a.order - b.order })

          $("#capture-container").loadTemplate($("#capture-template"), cams)

          $.each(cams, function(idx, data) {
            updateImage(data["name"])
            updateStatus(data["name"])
          })

          $("img.capture").one("load", function() {
            $("#capture-container").show();
            $("#capture-container").dragend({});
          });

          refreshWeatherData(false, function() {
            $("#conditions-container").show();
          });
        }
  });

}

$(function () {
    init();
});

$(window).on("load", function() {
    $("#loading").hide();
});