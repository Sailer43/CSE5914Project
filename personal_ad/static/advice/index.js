var startButton, stopButton, recorder;

window.onload = function () {
  startButton = document.getElementById('start');
  stopButton = document.getElementById('stop');

  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    startButton.disabled = false;
    startButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    recorder = new MediaRecorder(stream);

    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available
    recorder.addEventListener('dataavailable', onRecordingReady);
  });
};

function startRecording() {
  startButton.disabled = true;
  stopButton.disabled = false;

  recorder.start();
}

function stopRecording() {
  start.disabled = false;
  stopButton.disabled = true;

  // Stopping the recorder will eventually trigger the `dataavailable` event and we can complete the recording process
  recorder.stop();
}

function onRecordingReady(e) {
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });
  $.ajax({
    type: 'POST',
    url: 'advice/input_audio',
    data: e.data,
    processData: false,
    contentType: false,
    success: function (data) {
      c_audio = new Blob(data["audio"], {type: "audio/webm;codecs=opus"});
      input_text = data["input_text"]
      output_text = data["output_text"]
      external_link = data["external_link"]
      $("#chat_history").append("<p class='user_chat'>" + input_text + "</p>")
      if (external_link !== "") {
        $("#chat_history").append("<a href='" + external_link + "' class='assistant_chat'>" + output_text + "</a>")
      } else {
        $("#chat_history").append("<p class='assistant_chat'>" + output_text + "</p>")
      }
    }
  });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
