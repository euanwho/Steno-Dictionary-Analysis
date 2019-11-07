const csv = require('csv-parser');
const fs = require('fs');
const dictionary = [];
const wordList = [];
 
fs.createReadStream('data.csv')
  .pipe(csv(['English', 'Steno', 'Translates']))
  .on('data', (data) => dictionary.push(data))
  .on('end', () => {
    console.log(dictionary);
    // [
    //   { English: ', in other words', Steno: 'NOERDZ', Translates: '307' },
    // ]
  });

  fs.createReadStream('wordList.csv')
  .pipe(csv(['Word']))
  .on('data', (data) => wordList.push(data))
  .on('end', () => {
    console.log(wordList);
    // [
    //   { English: ', in other words', Steno: 'NOERDZ', Translates: '307' },
    // ]
  });

