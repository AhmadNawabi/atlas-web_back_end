const express = require('express');
const fs = require('fs').promises;

const app = express();
const port = 1245;

async function studentCounts(filePath) {
  try {
    const data = await fs.readFile(filePath, 'utf8');
    const lines = data.split('\n').filter((line) => line.trim() !== '');

    const { studentCount, fieldCounts } = lines.slice(1).reduce(
      (acc, line) => {
        const [firstName, , , field] = line.split(',').map((x) => x.trim());
        if (firstName) {
          acc.studentCount += 1;
          if (field === 'CS') acc.fieldCounts.CS.push(firstName);
          else if (field === 'SWE') acc.fieldCounts.SWE.push(firstName);
        }
        return acc;
      },
      { studentCount: 0, fieldCounts: { CS: [], SWE: [] } },
    );

    return 'This is the list of our students\n'
    + `Number of students: ${studentCount}\n`
    + `Number of students in CS: ${fieldCounts.CS.length}. List: ${fieldCounts.CS.join(', ')}\n`
    + `Number of students in SWE: ${fieldCounts.SWE.length}. List: ${fieldCounts.SWE.join(', ')}`;
  } catch (err) {
    throw new Error('Cannot load the database');
  }
}

app.get('/', (req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send('Hello Holberton School!');
});

app.get('/students', async (req, res) => {
  const dbPath = process.argv[2];

  try {
    const result = await studentCounts(dbPath);
    res.set('Content-Type', 'text/plain');
    res.send(result);
  } catch (error) {
    res.set('Content-Type', 'text/plain');
    res.send('Cannot load the database');
  }
});

app.listen(port, () => {
});

module.exports = app;
