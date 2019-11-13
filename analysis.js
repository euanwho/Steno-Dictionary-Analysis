module.exports = {
    analyseDictionary: function (wordList, dictionary) {
        // Iterates through wordList
        wordList.forEach(function (item, index) {
            var word = item;
            dictionary.forEach(function (item, index) {
                if (word.English == item.English) {
                        /*function analyseSteno(item) {
                        var regex = /#/;
                        if (regex.exec(item.Steno())){
                            console.log("true");
                        }*/
                    } 
                    console.log(word);
                }
            );
        }); 
    }
};
