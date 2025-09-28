const express = require('express');
require('dotenv').config()
var cors = require('cors')

const app = express();
app.use(cors())
app.disable('etag');

app.use(express.json());
app.get('/', (req, res) => {
  res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  res.send({ msg: 'Hello World' })
})
app.get('/health', (req, res) => {
  res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  res.send({ status: 'OK' })
})

app.listen(process.env.PORT, () => {
  console.log(`Server is running on port ${process.env.PORT}`);
});
