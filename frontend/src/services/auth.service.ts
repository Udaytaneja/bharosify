import type { UserProfile, UserRole } from '../types';
import { apiClient } from '../api/client';

export class AuthService {
  static async login(email: string, password = 'password'): Promise<{ userProfile: UserProfile; tokens: any }> {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { access_token, refresh_token, user } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      const role: UserRole = user.role === 'banker' ? 'banker' : 'applicant';
      const userProfile: UserProfile = {
        id: String(user.id),
        name: user.name || (role === 'banker' ? 'Vikram Singh' : 'Alex Mercer'),
        role,
        title: role === 'banker' ? 'Lead Underwriter / Risk Officer' : 'CFO, Apex Tech Corp',
        email: user.email,
        authLevel: role === 'banker' ? 'L3-AUTH' : undefined,
        accountStatus: 'VERIFIED',
      };

      localStorage.setItem('agenttrust_auth_user', JSON.stringify(userProfile));
      return { userProfile, tokens: response.data };
    } catch (err) {
      console.warn('Real API login fallback to mock:', err);
      // Fallback mock profile for development when backend user is not seeded
      const isBanker = email.includes('banker') || email.includes('vikram');
      const fallbackRole: UserRole = isBanker ? 'banker' : 'applicant';
      const fallbackProfile: UserProfile = isBanker
        ? {
            id: 'BKR-7749-NY',
            name: 'Vikram Singh',
            role: fallbackRole,
            title: 'Lead Underwriter / Risk Officer',
            email: email || 'vikram.singh@agenttrust.bank',
            authLevel: 'L3-AUTH',
          }
        : {
            id: 'APP-8942-NY',
            name: 'Alex Mercer',
            role: 'applicant',
            title: 'CFO, Apex Tech Corp',
            email: email || 'alex.mercer@apextech.com',
            accountStatus: 'VERIFIED',
          };

      localStorage.setItem('agenttrust_auth_user', JSON.stringify(fallbackProfile));
      return { userProfile: fallbackProfile, tokens: null };
    }
  }

  static async loginAsBanker(employeeId = 'BKR-7749-NY', password = 'password'): Promise<UserProfile> {
    const res = await this.login(employeeId.includes('@') ? employeeId : 'banker@agenttrust.bank', password);
    return res.userProfile;
  }

  static async loginAsApplicant(email = 'alex.mercer@apextech.com', password = 'password'): Promise<UserProfile> {
    const res = await this.login(email, password);
    return res.userProfile;
  }

  static async getCurrentSession(): Promise<UserProfile | null> {
    const saved = localStorage.getItem('agenttrust_auth_user');
    if (!saved) return null;
    try {
      return JSON.parse(saved);
    } catch {
      return null;
    }
  }

  static async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout');
    } catch {
      // Ignore network errors on logout
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('agenttrust_auth_user');
    }
  }
}
