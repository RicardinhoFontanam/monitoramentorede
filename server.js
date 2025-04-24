import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import fs from 'fs-extra';
import path from 'path';

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// Middleware de token
const TOKEN_VALIDO = "seu-token-aqui";

app.use('/api/send-data', (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (token !== TOKEN_VALIDO) {
    return res.status(403).json({ message: 'Token inválido' });
  }
  next();
});

// Rota para receber dados do agente
app.post('/api/send-data', async (req, res) => {
  const data = req.body;
  try {
    await fs.outputJson('./data/networkData.json', data, { spaces: 2 });
    res.status(200).json({ message: 'Dados recebidos com sucesso!' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Erro ao salvar os dados' });
  }
});

// Rota para fornecer dados ao frontend
app.get('/api/network-status', async (req, res) => {
  try {
    const data = await fs.readJson('./data/networkData.json');
    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(404).json({ message: 'Dados não encontrados' });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
