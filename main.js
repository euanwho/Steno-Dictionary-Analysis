const csv = require('csv-parser');
const fs = require('fs');
const dictionary = [];
const wordList = [];
const analysis = require('./analysis')
 
/*function dictionaryCreate(){
    fs.createReadStream('data.csv')
        .pipe(csv(['English', 'Steno', 'Translates']))
        .on('data', (data) => dictionary.push(data))
        .on('end', () => {
        // console.log(dictionary);
        // [
        //   { English: ', in other words', Steno: 'NOERDZ', Translates: '307' },
        // ]
 });
}
  
function wordListCreate() {
    fs.createReadStream('wordList.csv')
    .pipe(csv(['Word']))
    .on('data', (data) => wordList.push(data))
    .on('end', () => {
      console.log(wordList.length);
      // [
      //   { English: ', in other words', Steno: 'NOERDZ', Translates: '307' },
      // ]
});
}


// analysis.analyseDictionary(dictionary, wordList);

/* Write method to search dictionary for group of words, and if it is written in two strokes return it */

function what(dic, wordL) {
    wordL.forEach(function (item, index) {
        var word = item;
        dic.forEach(function (item, index) {
            if (word == item) {
                console.log(word);
            }
        });
    }); 
}

var a = [1, 2, 3, 2, 5];
var b = [9, 8, 7, 4, 5];

what(a, b);