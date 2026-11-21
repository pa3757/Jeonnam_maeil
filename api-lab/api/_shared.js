// Shared helpers for the API routes.
// Keys live only in Vercel environment variables (never sent to the browser).
// ACCESS_CODE gates the endpoints so a shared link can't spend the instructor's credits.

export function checkAccess(req, res) {
  const expected = process.env.ACCESS_CODE;
  if (!expected) {
    res.status(500).json({ error: '서버에 ACCESS_CODE가 설정되지 않았습니다. Vercel 환경 변수를 확인하세요.' });
    return false;
  }
  if (req.headers['x-access-code'] !== expected) {
    res.status(401).json({ error: '접속 코드가 맞지 않습니다.' });
    return false;
  }
  return true;
}

export function readBody(req) {
  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
  const prompt = String(b.prompt || '').trim();
  const system = String(b.system || '').trim();
  const model = String(b.model || '').trim();
  return { prompt, system, model };
}

export function guard(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'POST only' });
    return null;
  }
  if (!checkAccess(req, res)) return null;
  const body = readBody(req);
  if (!body.prompt) {
    res.status(400).json({ error: '프롬프트가 비어 있습니다.' });
    return null;
  }
  if (body.prompt.length > 20000) {
    res.status(400).json({ error: '프롬프트가 너무 깁니다 (20,000자 이하).' });
    return null;
  }
  return body;
}
