$(document).ready(function () {
  latestNews();
});
var latestNews = () => {
  // fetch to call news API
  fetch("/latest-news")
    .then((response) => response.json())
    .then((data) => {
      if (data.news) {
        const article = data.news;
        $("#news")
          .attr("href", article.url)
          .find(".news-title")
          .text("Latest news: " + article.title);
      } else {
        $("#news").hide(); // will hide if no news is caught
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      $("#news").hide(); // will hide if no news is caught
    });
};
