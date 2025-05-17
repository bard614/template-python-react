import { create } from 'zustand';
import api from '../api/axios';

const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post('/auth/login', {
        username: email,
        password,
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      
      // 獲取用戶資訊
      const userResponse = await api.get('/auth/me');
      const user = userResponse.data;
      
      set({
        user,
        isAuthenticated: true,
        isLoading: false,
      });
      
      return true;
    } catch (error) {
      set({
        error: error.response?.data?.detail || '登入失敗',
        isLoading: false,
      });
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({
      user: null,
      isAuthenticated: false,
    });
  },

  checkAuth: async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      set({ isAuthenticated: false });
      return;
    }

    try {
      const response = await api.get('/auth/me');
      set({
        user: response.data,
        isAuthenticated: true,
      });
    } catch (error) {
      localStorage.removeItem('token');
      set({
        user: null,
        isAuthenticated: false,
      });
    }
  },
}));

export default useAuthStore; 