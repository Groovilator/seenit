var reddit_posts = [];

function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x > y) ? -1 : ((x < y) ? 1 : 0));
    });
}

$("#query").click(function(event){
    $.getJSON('/topimages',
    {
        period: $('#period').val()
    }, 
    function (data) {
      reddit_posts = data;
      $("#top").prop("disabled", true);
      $("#pop").prop("disabled", false);
      generateTable(reddit_posts);
    });
});

$("#top").click(function(event){
    $("#top").prop("disabled", true);
    $("#pop").prop("disabled", false);

    reddit_posts = sortByKey(reddit_posts, 'Up Votes');

    generateTable(reddit_posts);
});

$("#pop").click(function(event){
    $("#pop").prop("disabled", true);
    $("#top").prop("disabled", false);

    reddit_posts = sortByKey(reddit_posts, 'Popularity Rating');

    generateTable(reddit_posts);
});

$(document).ready(function(event) {
    $.getJSON('/hotimages',
    function (data) {
      generateChart(data);
    });
});

function generateTable(posts) {
    console.log("generateTable");
    var col = ['Thumbnail', 'Title', 'Subreddit', 'Up Votes', 'Comment Count', 'Popularity Rating'];

    var table = document.createElement("table");

    var tr = table.insertRow(-1);

    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");
        th.innerHTML = col[i];
        tr.appendChild(th);
    }

    for (var i = 0; i < posts.length && i < 50; i++) {

        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            if (col[j] == 'Thumbnail'){
                tabCell.innerHTML="<img src='"+posts[i][col[j]]+"' />";
            }
            else if (col[j] == 'Title')
            {
                tabCell.innerHTML = '<a href="' + posts[i]["url"] + '">'+ posts[i][col[j]] +'</a>';
            }
            else{
                tabCell.innerHTML = posts[i][col[j]];
            }
        }
    }

    var divContainer = document.getElementById("topResults");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);
}

function generateChart(posts) {
    posts = sortByKey(posts, 'Up Votes');
    var sub_counts = {}
    for (var i = 0; i < posts.length && i < 50; i++) { 
        if (!(posts[i]["Subreddit"] in sub_counts)) {
            sub_counts[posts[i]["Subreddit"]] = 1;
        }
        else {
            sub_counts[posts[i]["Subreddit"]]++;
        }
    }
    var dp = [];
    Object.keys(sub_counts).forEach(function(key) {
        dp.push({
            x: 0,
            y: sub_counts[key],
            name: key
        });;
    });
    dp = sortByKey(dp, 'y');

    var chart = new CanvasJS.Chart("chartContainer",
    {
      title:{
      text: "Distribution of Subreddits contributing images to Hot/Rising"
      },

      axisY: {
        gridThickness:0,
        lineThickness:0,
        tickThickness:0,
        valueFormatString:" "
      },
      axisX: {
        gridThickness:0,
        lineThickness:0,
        tickThickness:0,
        valueFormatString:" "
      },

      data: [
      {
        type: "stackedBar100",
        toolTipContent: "{name}: <strong>{y}</strong>",
        dataPoints: dp
      }
      ]
    });

    chart.render();
}