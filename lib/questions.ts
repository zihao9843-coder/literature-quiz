import fs from 'fs';
import path from 'path';

export type Question = Record<string, string>;

export function loadQuestions(): Question[] {
  const p = path.join(process.cwd(), 'data', 'questions_generated.json');
  if (!fs.existsSync(p)) return [];
  return JSON.parse(fs.readFileSync(p, 'utf-8'));
}

export function loadWrongQuestions(): Question[] {
  return loadQuestions().filter((q) => q['是否错题'] === '是');
}
