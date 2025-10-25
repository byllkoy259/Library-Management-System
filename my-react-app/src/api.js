import axios from 'axios';
import keycloak from './keycloak';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

api.interceptors.request.use(
  async (config) => {
      if (keycloak.token) {
        await keycloak.updateToken(30); // Cập nhật token nếu sắp hết hạn trong 30 giây
        config.headers.Authorization = `Bearer ${keycloak.token}`;
      }
      return config;
  }, (error) => Promise.reject(error)
);

export const getProtectedData = async () => {
  try {
      const response = await api.get('/protected');
      return response.data;
  } catch (error) {
      console.error('API call failed:', error);
      throw error;
  }
};

// API cho categories
export const getCategories = async (search = '') => api.get(`/user/categories?search=${search}`).then(res => res.data);
export const getCategoriesAdmin = async (search = '') => api.get(`/admin/categories?search=${search}`).then(res => res.data);
export const createCategory = async (data) => api.post('/admin/categories', data).then(res => res.data);
export const updateCategory = async (id, data) => api.put(`/admin/categories/${id}`, data).then(res => res.data);
export const deleteCategory = async (id) => api.delete(`/admin/categories/${id}`).then(res => res.data);

// API cho books
export const getBooks = async (search = '') => api.get(`/user/books?search=${search}`).then(res => res.data);
export const getBookById = async (id) => api.get(`/user/books/${id}`).then(res => res.data);
export const getBooksAdmin = async (search = '') => api.get(`/admin/books?search=${search}`).then(res => res.data);
export const createBook = async (data) => api.post('/admin/books', data).then(res => res.data);
export const updateBook = async (id, data) => api.put(`/admin/books/${id}`, data).then(res => res.data);
export const deleteBook = async (id) => api.delete(`/admin/books/${id}`).then(res => res.data);

// API cho authors
export const getAuthors = async (search = '') => api.get(`/user/authors?search=${search}`).then(res => res.data);
export const getAuthorsAdmin = async (search = '') => api.get(`/admin/authors?search=${search}`).then(res => res.data);
export const createAuthor = async (data) => api.post('/admin/authors', data).then(res => res.data);
export const updateAuthor = async (id, data) => api.put(`/admin/authors/${id}`, data).then(res => res.data);
export const deleteAuthor = async (id) => api.delete(`/admin/authors/${id}`).then(res => res.data);

// API cho users (admin)
export const getUsers = async (search = '') => api.get(`/admin/users?search=${search}`).then(res => res.data);
export const createUser = async (data) => api.post('/admin/users', data).then(res => res.data);
export const updateUser = async (id, data) => api.put(`/admin/users/${id}`, data).then(res => res.data);
export const deleteUser = async (id) => api.delete(`/admin/users/${id}`).then(res => res.data);

// API cho việc mượn sách của người dùng
// Lưu ý: prefix /api đã được cấu hình trong axios instance (baseURL)
export const getCurrentBorrows = async () => api.get('/user/borrows/current').then(res => res.data);
export const getBorrowHistory = async () => api.get('/user/borrows/history').then(res => res.data);