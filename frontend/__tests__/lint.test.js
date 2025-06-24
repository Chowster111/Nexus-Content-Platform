import { execSync } from "child_process";
import { test, expect } from '@jest/globals';

test('Frontend code passes ESLint', () => {
  try {
    execSync('npx eslint . --ext .ts,.tsx --max-warnings=0', { stdio: 'pipe' });
  } catch (err) {
    const output = err.stdout.toString();
    throw new Error(`ESLint errors found:\n${output}`);
  }
});
