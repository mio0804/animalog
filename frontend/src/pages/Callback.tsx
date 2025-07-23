import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Container, Spinner, Alert } from 'react-bootstrap';
import { authAPI } from '../services/api';

const Callback: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const error = searchParams.get('error');

      if (error) {
        setError('認証エラーが発生しました');
        setTimeout(() => {
          navigate('/login');
        }, 3000);
        return;
      }

      if (!code) {
        setError('認証コードが見つかりません');
        setTimeout(() => {
          navigate('/login');
        }, 3000);
        return;
      }

      try {
        const response = await authAPI.callback(code);
        localStorage.setItem('token', response.token);
        navigate('/');
      } catch (err) {
        console.error('Callback error:', err);
        setError('認証処理中にエラーが発生しました');
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="text-center">
        {error ? (
          <>
            <Alert variant="danger">{error}</Alert>
            <p>ログインページに戻ります...</p>
          </>
        ) : (
          <>
            <Spinner animation="border" role="status" className="mb-3">
              <span className="visually-hidden">認証処理中...</span>
            </Spinner>
            <p>認証処理中です。しばらくお待ちください...</p>
          </>
        )}
      </div>
    </Container>
  );
};

export default Callback;