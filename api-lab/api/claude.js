import Anthropic from '@anthropic-ai/sdk';
import { guard } from './_shared.js';

// Plain Messages API call: no tools are declared, so Claude answers from its own
// knowledge only (no web search) - which is the point of this classroom test.
const MODELS = ['claude-opus-5-5', 'claude-sonnet-5-5', 'claude-haiku-5-5'];
// Models that support the server-side refusal fallback (beta).
const FALLBACK_MODELS = new Set(['claude-opus-5-5', 'claude-sonnet-5-5']);

const client = new Anthropic(); // reads ANTHROPIC_API_KEY

export default async function handler(req, res) {
  const body = guard(req, res);
  if (!body) return;
  const model = MODELS.includes(body.model) ? body.model : MODELS[0];
  const started = Date.now();

  const params = {
    model,
    max_tokens: 16000,
    output_config: { effort: 'medium' },
    messages: [{ role: 'user', content: body.prompt }],
    ...(body.system ? { system: body.system } : {}),
  };

  try {
    const response = FALLBACK_MODELS.has(model)
      ? await client.beta.messages.create({
          ...params,
          betas: ['server-side-fallback-2026-07-01'],
          fallbacks: 'default',
        })
      : await client.messages.create(params);

    const text = response.content
      .filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('\n')
      .trim();
    const fallbackRan = (response.usage?.iterations ?? []).some((e) => e.type === 'fallback_message');

    res.status(200).json({
      provider: 'claude',
      model: response.model,
      requestedModel: model,
      text,
      stopReason: response.stop_reason,
      refusal: response.stop_reason === 'refusal' ? response.stop_details ?? null : null,
      fallbackRan,
      usage: { input: response.usage?.input_tokens ?? null, output: response.usage?.output_tokens ?? null },
      ms: Date.now() - started,
    });
  } catch (error) {
    let status = 500;
    let message = '알 수 없는 오류';
    if (error instanceof Anthropic.APIConnectionError) {
      status = 502;
      message = 'Claude 서버에 연결하지 못했습니다. 잠시 후 다시 시도하세요.';
    } else if (error instanceof Anthropic.AuthenticationError) {
      status = 500;
      message = 'Claude API 키가 올바르지 않습니다 (ANTHROPIC_API_KEY 확인).';
    } else if (error instanceof Anthropic.RateLimitError) {
      status = 429;
      message = 'Claude API 사용량 한도에 걸렸습니다. 잠시 후 다시 시도하세요.';
    } else if (error instanceof Anthropic.BadRequestError) {
      status = 400;
      message = `요청 오류: ${error.message}`;
    } else if (error instanceof Anthropic.APIError) {
      status = error.status ?? 500;
      message = `Claude API 오류 (${error.status}): ${error.message}`;
    } else if (error instanceof Error) {
      message = error.message;
    }
    res.status(status).json({ provider: 'claude', error: message, ms: Date.now() - started });
  }
}
