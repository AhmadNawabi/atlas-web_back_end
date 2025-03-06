const http = require('http');
const fs = require('fs');

const databaseFile = process.argv[2];

const app = http.createServer((req, res) => {
  if (req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.write('Hello Holberton School!');
    res.end();
  } else if (req.url === '/students') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.write('This is the list of our students\n');

    fs.readFile(databaseFile, 'utf8', (err, data) => {
      if (err) {
        res.write('Cannot load the database');
        res.end();
        return;
      }

      const lines = data.split('\n').filter((line )=> line.trim() !== '');
      const students = lines.slice(1).map((line) => line.split(','));

      res.write(`Number of students: ${students.length}\n`);
      const fields = lines[0].split(',');

      const studentGroups = students.reduce((acc, studentData) => {
        const field = studentData[fields.indexOf('field')];
        if (!acc[field]) {
          acc[field] = [];
        }
        acc[field].push(studentData[fields.indexOf('firstname')]);
        return acc;
      }, {});

      for (const [field, names] of Object.entries(studentGroups)) {
        res.write(`Number of students in ${field}: ${names.length}. List: ${names.join(', ')}\n`);
      }

      res.end();
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.write('Not found');
    res.end();
  }
});

app.listen(1245);
module.exports = app;
