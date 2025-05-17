import { create } from 'zustand';
import axios from '../utils/axios';

const useUserStore = create((set, get) => ({
  users: [],
  isLoading: false,
  error: null,

  fetchUsers: async ({ search = '', sort_by = 'id', order = 'asc' } = {}) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get('/users', {
        params: { search, sort_by, order }
      });
      set({ users: response.data, isLoading: false });
    } catch (error) {
      set({
        error: error.response?.data?.detail || '載入使用者資料時發生錯誤',
        isLoading: false
      });
    }
  },

  createUser: async (userData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post('/users', userData);
      set((state) => ({
        users: [...state.users, response.data],
        isLoading: false
      }));
      return response.data;
    } catch (error) {
      set({
        error: error.response?.data?.detail || '建立使用者時發生錯誤',
        isLoading: false
      });
      throw error;
    }
  },

  updateUser: async (userId, userData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.put(`/users/${userId}`, userData);
      set((state) => ({
        users: state.users.map((user) =>
          user.id === userId ? response.data : user
        ),
        isLoading: false
      }));
      return response.data;
    } catch (error) {
      set({
        error: error.response?.data?.detail || '更新使用者時發生錯誤',
        isLoading: false
      });
      throw error;
    }
  },

  deleteUser: async (userId) => {
    set({ isLoading: true, error: null });
    try {
      await axios.delete(`/users/${userId}`);
      set((state) => ({
        users: state.users.filter((user) => user.id !== userId),
        isLoading: false
      }));
    } catch (error) {
      set({
        error: error.response?.data?.detail || '刪除使用者時發生錯誤',
        isLoading: false
      });
      throw error;
    }
  },

  clearError: () => set({ error: null })
}));

export default useUserStore; 