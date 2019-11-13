const csv = require('csv-parser');
const fs = require('fs');
const dictionary = [];
const wordList = [];
const analysis = require('./analysis')
 
function dictionaryCreate(){
    fs.createReadStream('data.csv')
        .pipe(csv(['English', 'Steno', 'Translates']))
        .on('data', (data) => dictionary.push(data))
        .on('end', () => {
         console.log(dictionary);
        // [
        //   { English: ', in other words', Steno: 'NOERDZ', Translates: '307' },
        // ]
 });
}
  
function wordListCreate() {
    fs.createReadStream('wordList.csv')
    .pipe(csv())
    .on('data', (data) => wordList.push(data))
    .on('end', () => {
      console.log(wordList);
      // [
      //   { English: ', in other words', Steno: 'NOERDZ', Translates: '307' },
      // ]
});
}


wordListCreate();
dictionaryCreate();
console.log(dictionary, wordList);
analysis.analyseDictionary(dictionary, wordList);

var a = [{ English: 1, Steno: "#1"}, {English: 2, Steno: "#2"}];
var b = [{English: 3, Steno: "#3"}, {English: 1, Steno: "#3"}];

// analysis.analyseDictionary(a, b);