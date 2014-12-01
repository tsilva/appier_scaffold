$(document).ready(function() {
    var filterE = $(".filter");
    var dietE = $(".drop-field.diet");
    var groupE = $(".drop-field.food-group");
    var refreshList = function() {
        var elemE = $(this);
        var groupId = $(".hidden-field", groupE).uxvalue();
        var filters = [];
        if(groupId) filters.push(["groups_l", "contains", [groupId]]);
        filterE.data("filters", filters);
        filterE.triggerHandler("update");
    };

    var listRefreshedHandler = function() {
        $("li", filterE).each(function(index, value) {
            // retrieves the levels for the entry,
            // continuing in case there are none
            var elemE = $(value);
            var inputLevelsJE = $("input.levels-j", elemE);
            var spanE = $("span", elemE);
            var levelsJ = inputLevelsJE.uxvalue();
            if(levelsJ == "-") levelsJ = "[]";
            if(levelsJ.indexOf("%") == 0) return;
            var levels = jQuery.parseJSON(levelsJ);
            if(!levels) return;

            // retrieves the currently selected diet
            var dietId = $("input", dietE).uxvalue();
            dietId = parseInt(dietId);

            // searches for the level of the selected diet
            for(var index = 0; index < levels.length; index++) {
                // continues in case this is not
                // the level for the selected diet
                var level = levels[index];
                var _dietId = level[0];
                var level = level[1];
                if(dietId != _dietId) continue;

                // @TODO: softcode this
                var levelS = "";
                if(level == 1) levelS = "Allowed";
                else if(level == 2) levelS = "Caution";
                else if(level === 3) levelS = "Denied";
                var levelL = levelS.toLowerCase();

                // updates the level in the entry
                // and returns (entry found)
                spanE.removeClass();
                spanE.addClass(levelL);
                spanE.uxvalue(levelS);
                return;
            }

            var inputLevelSE = $("input.level-s", elemE);
            var levelS = inputLevelSE.uxvalue();
            if(levelS == null || levelS == "") levelS = "-";
            var levelL = levelS.toLowerCase();
            spanE.removeClass();
            spanE.addClass(levelL);
            spanE.uxvalue(levelS);
        });
    };

    dietE.bind("value_select", refreshList);
    groupE.bind("value_select", refreshList);
    groupE.bind("value_unselect", refreshList);
    filterE.bind("update_complete", listRefreshedHandler);
    var foodName = $(".food-name").uxvalue();
    if(foodName) $("ul .filter-input").uxvalue(foodName);
    refreshList();
});
