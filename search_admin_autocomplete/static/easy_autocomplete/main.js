$(function () {
    var options = {
        url: function (phrase) {
            return "search/" + phrase;
        },
        getValue: "keyword",

        template: {
            type: "links",
            fields: {
                link: "url"
            }
        },
        list: {
            maxNumberOfElements: 6,
            onChooseEvent: function () {
                var config = window.SEARCH_ADMIN_CONFIG || { redirectToDetail: false };
                if (config.redirectToDetail) {
                    location.href = $('#searchbar').getSelectedItemData().url;
                } else {
                    $('#changelist-search').submit();
                }
            },
            match: {
                enabled: true
            }
        }

    };
    $("#searchbar").easyAutocomplete(options);
})