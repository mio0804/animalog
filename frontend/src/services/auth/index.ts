// 認証サービスのファクトリー

import { type AuthService } from './types.ts';
import { CognitoAuthService } from './CognitoAuthService.ts';
import { MockAuthService } from './MockAuthService.ts';

// 環境変数に基づいて適切な認証サービスを作成
export function createAuthService(): AuthService {
  const useCognito = import.meta.env.VITE_USE_COGNITO === 'true';
  
  if (useCognito) {
    console.log('Using Cognito authentication');
    return new CognitoAuthService();
  } else {
    console.log('Using mock authentication for development');
    return new MockAuthService();
  }
}

// 型の再エクスポート
export type { AuthService, User } from './types.ts';