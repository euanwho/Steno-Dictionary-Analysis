const csv = require('csv-parser');
const fs = require('fs');
const results = [];
 
fs.createReadStream('data.csv')
  .pipe(csv(['English', 'Steno', 'Translates']))
  .on('data', (data) => results.push(data))
  .on('end', () => {
    console.log(results);
    // [
    //   { English: ', in other words', Steno: 'NOERDZ', Translates: '307' },
    //   { NAME: 'Bugs Bunny', AGE: '22' }
    // ]
  });