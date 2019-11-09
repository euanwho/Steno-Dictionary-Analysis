module.exports = {
    analyseDictionary: function (dic, wordL) {
        wordL.forEach(function (item, index) {
            var word = item;
            dic.forEach(function (item, index) {
                if (word == item) {
                    console.log(word);
                }
            });
        }); 
    },
    
  };
