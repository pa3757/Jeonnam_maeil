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
  const openaiDefault = preferred && openai.some((m) => m.id === preferred) ? preferred : openai[0]?.id ?? preferred ?? null;
  res.status(200).json({
    claude: CLAUDE,
    claudeDefault: CLAUDE[0].id,
    openai: openai.map((m) => ({ id: m.id, label: m.id })),
    openaiDefault,
    openaiError,
  });
}
