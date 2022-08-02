    var data = [
    {
        "tags": [
            "change",
            "deep-thoughts",
            "thinking",
            "world"
        ],
        "author": {
            "name": "Albert Einstein",
            "goodreads_link": "/author/show/9810.Albert_Einstein",
            "slug": "Albert-Einstein"
        },
        "text": "\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d"
    },
    {
        "tags": [
            "abilities",
            "choices"
        ],
        "author": {
            "name": "J.K. Rowling",
            "goodreads_link": "/author/show/1077326.J_K_Rowling",
            "slug": "J-K-Rowling"
        },
        "text": "\u201cIt is our choices, Harry, that show what we truly are, far more than our abilities.\u201d"
    },
    {
        "tags": [
            "inspirational",
            "life",
            "live",
            "miracle",
            "miracles"
        ],
        "author": {
            "name": "Albert Einstein",
            "goodreads_link": "/author/show/9810.Albert_Einstein",
            "slug": "Albert-Einstein"
        },
        "text": "\u201cThere are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.\u201d"
    },
    {
        "tags": [
            "aliteracy",
            "books",
            "classic",
            "humor"
        ],
        "author": {
            "name": "Jane Austen",
            "goodreads_link": "/author/show/1265.Jane_Austen",
            "slug": "Jane-Austen"
        },
        "text": "\u201cThe person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.\u201d"
    },
    {
        "tags": [
            "be-yourself",
            "inspirational"
        ],
        "author": {
            "name": "Marilyn Monroe",
            "goodreads_link": "/author/show/82952.Marilyn_Monroe",
            "slug": "Marilyn-Monroe"
        },
        "text": "\u201cImperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.\u201d"
    },
    {
        "tags": [
            "adulthood",
            "success",
            "value"
        ],
        "author": {
            "name": "Albert Einstein",
            "goodreads_link": "/author/show/9810.Albert_Einstein",
            "slug": "Albert-Einstein"
        },
        "text": "\u201cTry not to become a man of success. Rather become a man of value.\u201d"
    },
    {
        "tags": [
            "life",
            "love"
        ],
        "author": {
            "name": "Andr\u00e9 Gide",
            "goodreads_link": "/author/show/7617.Andr_Gide",
            "slug": "Andre-Gide"
        },
        "text": "\u201cIt is better to be hated for what you are than to be loved for what you are not.\u201d"
    },
    {
        "tags": [
            "edison",
            "failure",
            "inspirational",
            "paraphrased"
        ],
        "author": {
            "name": "Thomas A. Edison",
            "goodreads_link": "/author/show/3091287.Thomas_A_Edison",
            "slug": "Thomas-A-Edison"
        },
        "text": "\u201cI have not failed. I've just found 10,000 ways that won't work.\u201d"
    },
    {
        "tags": [
            "misattributed-eleanor-roosevelt"
        ],
        "author": {
            "name": "Eleanor Roosevelt",
            "goodreads_link": "/author/show/44566.Eleanor_Roosevelt",
            "slug": "Eleanor-Roosevelt"
        },
        "text": "\u201cA woman is like a tea bag; you never know how strong it is until it's in hot water.\u201d"
    },
    {
        "tags": [
            "humor",
            "obvious",
            "simile"
        ],
        "author": {
            "name": "Steve Martin",
            "goodreads_link": "/author/show/7103.Steve_Martin",
            "slug": "Steve-Martin"
        },
        "text": "\u201cA day without sunshine is like, you know, night.\u201d"
    }
];
    for (var i in data) {
        var d = data[i];
        var tags = $.map(d['tags'], function(t) {
            return "<a class='tag'>" + t + "</a>";
        }).join(" ");
        document.write("<div class='quote'><span class='text'>" + d['text'] + "</span><span>by <small class='author'>" + d['author']['name'] + "</small></span><div class='tags'>Tags: " + tags + "</div></div>");
        }
