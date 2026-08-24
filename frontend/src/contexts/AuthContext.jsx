import { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Optimistically restore cached user for instant UI render,
    // then verify the session with the backend.
    const cached = localStorage.getItem('user');
    if (cached) {
      try {
        setUser(JSON.parse(cached));
      } catch {
        localStorage.removeItem('user');
      }
    }
    verifySession();

    // auth:expired is dispatched by the API interceptor when a refresh attempt
    // fails — clear state here instead of doing a hard page redirect.
    const handleExpired = () => {
      setUser(null);
      localStorage.removeItem('user');
    };
    window.addEventListener('auth:expired', handleExpired);
    return () => window.removeEventListener('auth:expired', handleExpired);
  }, []);

  const verifySession = async () => {
    try {
      const response = await api.getCurrentUser();
      setUser(response.data);
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch {
      // Token missing, expired, or invalid — clear stale cache
      setUser(null);
      localStorage.removeItem('user');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      const response = await api.login(username, password);
      const { user: userData } = response.data;
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed';
      throw new Error(errorMessage);
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await api.register(username, email, password);
      const { user: userData } = response.data;
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Registration failed';
      throw new Error(errorMessage);
    }
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch {
      // Ignore logout errors — clear state regardless
    }
    setUser(null);
    localStorage.removeItem('user');
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
