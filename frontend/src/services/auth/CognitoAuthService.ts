// AWS Cognito認証サービス

import { Amplify } from 'aws-amplify';
import { signInWithRedirect, signOut, getCurrentUser, fetchAuthSession } from 'aws-amplify/auth';
import { type AuthService, type User } from './types.ts';

export class CognitoAuthService implements AuthService {
  constructor() {
    // コンストラクタは空
  }

  async initialize(): Promise<void> {
    const config = {
      Auth: {
        Cognito: {
          userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || '',
          userPoolClientId: import.meta.env.VITE_COGNITO_CLIENT_ID || '',
          loginWith: {
            oauth: {
              domain: import.meta.env.VITE_COGNITO_DOMAIN || '',
              scopes: ['openid', 'email', 'profile'],
              redirectSignIn: [import.meta.env.VITE_COGNITO_REDIRECT_URI || 'http://localhost:3000/callback'],
              redirectSignOut: [import.meta.env.VITE_COGNITO_LOGOUT_URI || 'http://localhost:3000/login'],
              responseType: 'code',
            }
          }
        }
      }
    };
    
    Amplify.configure(config);
    console.log('CognitoAuthService initialized');
  }

  async getCurrentUser(): Promise<User | null> {
    try {
      console.log('CognitoAuthService: Getting current user...');
      const user = await getCurrentUser();
      console.log('CognitoAuthService: User found:', user.username);
      
      const attributes = user.signInDetails?.loginId || user.username;
      
      return {
        id: user.userId,
        email: attributes,
        username: user.username,
      };
    } catch (error: any) {
      // ユーザーが認証されていない場合は通常のフロー
      if (error.name === 'UserUnAuthenticatedException' || error.name === 'NotAuthorizedException') {
        console.log('CognitoAuthService: No authenticated user');
        return null;
      }
      console.error('CognitoAuthService: Error getting current user:', error);
      return null;
    }
  }

  async signIn(): Promise<void> {
    // Cognito Hosted UIへのリダイレクト
    await signInWithRedirect();
  }

  async signOut(): Promise<void> {
    await signOut();
  }

  async handleCallback(code: string): Promise<void> {
    // Amplifyが自動的にコールバックを処理するため、特別な処理は不要
    console.log('Cognito callback handler - Amplify will handle this automatically');
  }

  async getIdToken(): Promise<string | null> {
    try {
      const session = await fetchAuthSession();
      return session.tokens?.idToken?.toString() || null;
    } catch (error) {
      console.error('Failed to get ID token:', error);
      return null;
    }
  }
}