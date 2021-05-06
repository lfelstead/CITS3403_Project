const NUMBER_OF_HEADER_ITEMS = 6 // Not including Register/Login

/* Document Ready: */
$(document).ready(() => {
  // Load on page specific scripts
  switch(window.location.pathname) {
    case "/home":
      $("#debug").text("test");
      break;
    case "/one":
      break;
    case "quiz":
      break;
    default:
  }
  setHeader();
});

function topicInit() {

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
