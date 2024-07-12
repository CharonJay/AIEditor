import axios from 'axios';

export async function refreshToken() {
  try {
    console.log('refreshing token...');
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await axios.post('http://localhost:8000/user/token/refresh', {
      refresh: refreshToken
    });
    const newAccessToken = response.data.access;
    localStorage.setItem('access_token', newAccessToken);
    return newAccessToken;
  } catch (error) {
    // 处理刷新失败，例如重定向到登录页面
    console.error('Failed to refresh token:', error);
    return null;
  }
}