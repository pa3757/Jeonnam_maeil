import OpenAI from 'openai';
import { checkAccess } from './_shared.js';

// Returns the model choices for both columns.
// Claude: fixed list of current models. OpenAI: discovered from the account's
// /v1/models so the dropdown matches what the key can actually use.
const CLAUDE = [
  { id: 'claude-opus-5-5', label: 'Claude Opus 5.5 (기본)' },
  { id: 'claude-sonnet-5-5', label: 'Claude Sonnet 5.5' },
  { id: 'claude-haiku-5-5', label: 'Claude Haiku 5.5' },
];
// Built-in ChatGPT choices (IDs from OpenAI's model docs). The account's live
// list is shown first when it loads; these keep the dropdown usable without it.
export const OPENAI_BUILTIN = [
  { id: 'gpt-5.5', label: 'GPT-5.5' },
  { id: 'gpt-5', label: 'GPT-5' },
  { id: 'gpt-5-mini', label: 'GPT-5 mini' },
  { id: 'gpt-5-nano', label: 'GPT-5 nano' },
  { id: 'gpt-5-chat-latest', label: 'GPT-5 Chat (ChatGPT 기본 모델 별칭)' },
];
const EXCLUDE = /search|realtime|audio|tts|transcribe|image|embedding|moderation|dall-e|whisper|instruct|codex|davinci|babbage|computer-use/i;

export default async function handler(req, res) {
  if (!checkAccess(req, res)) return;
  let openai = [];
  let openaiError = null;
  try {
    const client = new OpenAI();
    for await (const m of client.models.list()) {
      if (/^(gpt-|o\d|chatgpt-)/.test(m.id) && !EXCLUDE.test(m.id)) openai.push({ id: m.id, created: m.created });
    }
    openai.sort((a, b) => (b.created ?? 0) - (a.created ?? 0));
  } catch (e) {
    openaiError = e instanceof Error ? e.message : String(e);
  }
  const preferred = process.env.OPENAI_MODEL;
  const ids = new Set(openai.map((m) => m.id));
  const openaiDefault =
    (preferred && (ids.has(preferred) || !openai.length) && preferred) ||
    OPENAI_BUILTIN.find((m) => ids.has(m.id))?.id ||
    openai[0]?.id ||
    OPENAI_BUILTIN[0].id;
  res.status(200).json({
    claude: CLAUDE,
    claudeDefault: CLAUDE[0].id,
    openai: openai.map((m) => ({ id: m.id, label: m.id })),
    openaiBuiltin: OPENAI_BUILTIN,
    openaiDefault,
    openaiError,
  });
}
