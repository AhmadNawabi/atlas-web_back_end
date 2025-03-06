const express = require('express');

const app = express();

app.get('/', (req, res) => {
  res.send('Hello Holberton School!');
});

app.use((req, res) => {
  const { path } = req;
  res.status(404).send(`Cannot GET ${path}`);
});

app.listen(1245);

module.exports = app;
