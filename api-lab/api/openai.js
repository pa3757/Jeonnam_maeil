import OpenAI from 'openai';
import { guard } from './_shared.js';

// Responses API call with no tools: the model answers from its own knowledge
// only (no web search). Model ids are discovered from the account (see /api/models),
// so this file doesn't hard-code a model list that would go stale.

const client = new OpenAI(); // reads OPENAI_API_KEY

export default async function handler(req, res) {
  const body = guard(req, res);
  if (!body) return;
  const model = body.model || process.env.OPENAI_MODEL;
  if (!model) {
    res.status(400).json({ provider: 'openai', error: 'ChatGPT 모델을 선택하세요.' });
    return;
  }
  if (!/^[A-Za-z0-9._:-]{1,80}$/.test(model)) {
    res.status(400).json({ provider: 'openai', error: '모델 ID 형식이 올바르지 않습니다.' });
    return;
  }
  if (/search|realtime|audio|tts|transcribe|image|embedding/i.test(model)) {
    res.status(400).json({ provider: 'openai', error: '검색·음성·이미지 전용 모델은 이 테스트에서 쓰지 않습니다.' });
    return;
  }
  const started = Date.now();
  try {
    const response = await client.responses.create({
      model,
      input: body.prompt,
      ...(body.system ? { instructions: body.system } : {}),
      max_output_tokens: 8000,
    });
    res.status(200).json({
      provider: 'openai',
      model: response.model,
      requestedModel: model,
      text: (response.output_text || '').trim(),
      stopReason: response.status === 'incomplete' ? `incomplete: ${response.incomplete_details?.reason ?? ''}` : response.status,
      usage: { input: response.usage?.input_tokens ?? null, output: response.usage?.output_tokens ?? null },
      ms: Date.now() - started,
    });
  } catch (error) {
    let status = 500;
    let message = '알 수 없는 오류';
    if (error instanceof OpenAI.APIConnectionError) {
      status = 502;
      message = 'OpenAI 서버에 연결하지 못했습니다. 잠시 후 다시 시도하세요.';
    } else if (error instanceof OpenAI.AuthenticationError) {
      message = 'OpenAI API 키가 올바르지 않습니다 (OPENAI_API_KEY 확인).';
    } else if (error instanceof OpenAI.RateLimitError) {
      status = 429;
      message = 'OpenAI API 사용량 한도에 걸렸습니다. 잠시 후 다시 시도하세요.';
    } else if (error instanceof OpenAI.APIError) {
      status = error.status ?? 500;
      message = `OpenAI API 오류 (${error.status}): ${error.message}`;
    } else if (error instanceof Error) {
      message = error.message;
    }
    res.status(status).json({ provider: 'openai', error: message, ms: Date.now() - started });
  }
}
