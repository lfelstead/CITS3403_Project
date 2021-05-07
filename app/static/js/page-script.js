const NUMBER_OF_HEADER_ITEMS = 6 // Not including Register/Login

/* Document Ready: */
$(document).ready(() => {
  // Stops saving requests to cache
  // Can/Shoul be removed once json files are finalised
  $.ajaxSetup({cache : false});

  // Load on page specific scripts
  switch(window.location.pathname) {
    case "/home":
      $("#debug").text("test");
      break;
    case "/one":
      topicQuizInit(quizNumber=0);
      break;
    case "quiz":
      break;
    default:
  }
  setHeader();
});

function topicQuizInit(quizNumber=null) {
  $("#debug").text(quizNumber);

  $(".quiz-button").click(() => {
    // FOR DEBUGGING:
    // $("#debug").text(quizNumber);
    // AJAX Request for question
    $.getJSON("../../static/json/questions.json", success = (data) => {
      let questionObj = data.practice[quizNumber];
      // FOR DEBUGGING: 
      // console.log(data)
      let builtString = "<p class='quiz-question'>" + questionObj.question + "<p>";
      builtString += "<p class='quiz-values'>Values: " + questionObj["default-values"] + "</p>";
      // Input:
      // Button for checking solution:

      $(".quiz-button").after(builtString);
    });
    
  });
}

/**
 * Sets active class to header item corrosponding to current page     \
 * Does not apply to login/register buttons but login/register pages
 * should disable all active classes                                  \
 */
function setHeader() {
  // Remove active class from any element in header
  $("#main-header ul a.active").removeClass("active");
  
  // Add active class to corrosponding header item
  let $headerItems = $("#main-header ul a");
  for(let i = 0; i < NUMBER_OF_HEADER_ITEMS; i++) {
    if(window.location.pathname == $headerItems[i].pathname)
      $($headerItems[i]).addClass("active");
  }
}
