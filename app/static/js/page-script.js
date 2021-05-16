const NUMBER_OF_HEADER_ITEMS = 6; // Not including Register/Login
const NUMBER_OF_TOPICS = NUMBER_OF_HEADER_ITEMS - 2;

/* Document Ready: */
$(document).ready(() => {
  loadProgressBar();

  // Stops saving requests to cache
  // Can/Should be removed once json files are finalised
  $.ajaxSetup({cache : false});

  // Load on page specific scripts
  switch(window.location.pathname) {
    case "/home":
      break;
    case "/one":
      quizNumber = 0;
      break;
    case "/two":
      quizNumber = 1;
      break;
    case "/three":
      quizNumber = 2;
      break;
    case "/four":
      quizNumber = 3;
      break;
    case "quiz":
      break;
    default:
  }
  // Topic specific elements
  if(typeof quizNumber !== 'undefined') {
    topicQuizInit(quizNumber);
  }

  // Set Validation for numerical input forms.
  let $input = $(".quiz-input");
  $input.attr("pattern", "^\\d*\\.?\\d+$");
  $input.attr("oninvalid", "this.setCustomValidity('Answer must be in an integer or a decimal layout.')");
});

/**
 * Initialises the practice question at the end of each topic page
 * @param quizNumber : [0:3] Which quiz topic is it 
 */
function topicQuizInit(quizNumber) {
  // Show the quiz container
  $(".practice-quiz-container").css("display", "inline-block");
  let $button = $("#show-quiz");
  $button.click(() => {

    // AJAX Request for question
    $.getJSON("../../static/json/questions.json", success = (data) => {
      let questionObj = data.practice[quizNumber];

      let htmlString = "<p class='quiz-question'>" + questionObj.question + "</p>";
      htmlString += "<p class='quiz-values'>Values: " + questionObj["default-values"] + "</p>";
      // Diagram
      htmlString += "<img class='quiz-diagram' src='" + questionObj.diagram + "'>";

      
      $button.after(htmlString);
      $button.hide("fast", "linear");

      $(".practice-quiz-container form").show();
      $(".units").html(questionObj.units); // Show units

      
      $(".practice-form").submit((event) => {
        let input = $("#practice-answer").val();
        submitPractice(quizNumber, input, questionObj.answer);
        event.preventDefault();
      });
      $(".practice-quiz-container").css("display", "grid"); // MAKES GRID
    }).fail(() => {alert("An error has occured");});
  });
}

function submitPractice(quizNumber, input, answer) {
  // Initialise localStorage entry for progress
  if(localStorage.getItem('progress') === null) {
    let array = new Array(NUMBER_OF_TOPICS).fill(false);
    localStorage.setItem('progress', JSON.stringify(array));
  }
  let progress = JSON.parse(localStorage.getItem('progress'));
  progress[quizNumber] = true;
  localStorage.setItem('progress', JSON.stringify(progress));
  loadProgressBar();
}


/**
 * To use a progress value to (re)load the progress bar
 * Also changes header to show which topics are completed
 * @param localOveride To override the local value
 */
function loadProgressBar(localOveride=null) {
  // 
  $(".header-dropdown-content a.finished").removeClass("finished");

  let progress = 0;
  if(localStorage.getItem('progress') !== null && localOveride === null) {
    let progressArray = JSON.parse(localStorage.getItem('progress'));
    let $headerItems = $(".header-dropdown-content a");
    for(var i = 0; i < NUMBER_OF_TOPICS; i++) {
      if(progressArray[i]) {
        progress++;
        $($headerItems[i]).addClass("finished");
      }
    }
  }
  // OVERRIDE:
  if(localOveride !== null) {
    progress = localOveride
  }


  let percentage = progress / NUMBER_OF_TOPICS * 100 + "%";
  $("#progress-bar").css("height", percentage);
}

/**
 * Reset progress bar
 */
function resetProgress() {
  let array = new Array(NUMBER_OF_TOPICS).fill(false);
  localStorage.setItem('progress', JSON.stringify(array));
  loadProgressBar();
}