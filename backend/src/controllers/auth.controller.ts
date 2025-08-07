import { Request, Response } from 'express';
import { AuthService } from '../services/auth.service';
import { UserModel } from '../models/user.model';

export class AuthController {
  private authService: AuthService;
  private userModel: UserModel;

  constructor() {
    this.authService = new AuthService();
    this.userModel = new UserModel();
  }

  /**
   * Register a new user
   */
  register = async (req: Request, res: Response) => {
    try {
      const { email, password, firstName, lastName, companyName, accountType } = req.body;

      // Validate required fields
      if (!email || !password) {
        return res.status(400).json({ message: 'Email and password are required' });
      }

      // Register user
      const user = await this.authService.register({
        email,
        password,
        firstName,
        lastName,
        companyName,
        accountType,
      });

      // Return success
      return res.status(201).json({
        message: 'User registered successfully',
        userId: user.id,
      });
    } catch (error: any) {
      return res.status(400).json({ message: error.message });
    }
  };

  /**
   * Login user
   */
  login = async (req: Request, res: Response) => {
    try {
      const { email, password } = req.body;

      // Validate required fields
      if (!email || !password) {
        return res.status(400).json({ message: 'Email and password are required' });
      }

      // Login user
      const { user, accessToken, refreshToken } = await this.authService.login(email, password);

      // Return tokens
      return res.status(200).json({
        message: 'Login successful',
        userId: user.id,
        accessToken,
        refreshToken,
      });
    } catch (error: any) {
      return res.status(401).json({ message: error.message });
    }
  };

  /**
   * Refresh token
   */
  refreshToken = async (req: Request, res: Response) => {
    try {
      const { refreshToken } = req.body;

      // Validate required fields
      if (!refreshToken) {
        return res.status(400).json({ message: 'Refresh token is required' });
      }

      // Refresh token
      const { user, accessToken, refreshToken: newRefreshToken } = await this.authService.refreshToken(refreshToken);

      // Return new tokens
      return res.status(200).json({
        userId: user.id,
        accessToken,
        refreshToken: newRefreshToken,
      });
    } catch (error: any) {
      return res.status(401).json({ message: error.message });
    }
  };

  /**
   * Logout user
   */
  logout = async (req: Request, res: Response) => {
    try {
      const { refreshToken } = req.body;

      // Validate required fields
      if (!refreshToken) {
        return res.status(400).json({ message: 'Refresh token is required' });
      }

      // Logout user
      await this.authService.logout(refreshToken);

      // Return success
      return res.status(200).json({ message: 'Logout successful' });
    } catch (error: any) {
      return res.status(500).json({ message: error.message });
    }
  };

  /**
   * Get current user profile
   */
  getProfile = async (req: Request, res: Response) => {
    try {
      if (!req.userId) {
        return res.status(401).json({ message: 'Authentication required' });
      }

      // Get user profile
      const userProfile = await this.userModel.getFullProfile(req.userId);

      // Remove sensitive information
      if (userProfile) {
        delete userProfile.passwordHash;
      }

      // Return user profile
      return res.status(200).json(userProfile);
    } catch (error: any) {
      return res.status(500).json({ message: error.message });
    }
  };

  /**
   * Update user profile
   */
  updateProfile = async (req: Request, res: Response) => {
    try {
      if (!req.userId) {
        return res.status(401).json({ message: 'Authentication required' });
      }

      const { profile, business, lenderProfile, borrowerProfile } = req.body;

      // Update profiles in transaction
      await Promise.all([
        profile && this.userModel.createOrUpdateProfile(req.userId, profile),
        business && this.userModel.createOrUpdateBusiness(req.userId, business),
        lenderProfile && this.userModel.createOrUpdateLenderProfile(req.userId, lenderProfile),
        borrowerProfile && this.userModel.createOrUpdateBorrowerProfile(req.userId, borrowerProfile),
      ]);

      // Get updated profile
      const updatedProfile = await this.userModel.getFullProfile(req.userId);

      // Return updated profile
      return res.status(200).json({
        message: 'Profile updated successfully',
        profile: updatedProfile,
      });
    } catch (error: any) {
      return res.status(500).json({ message: error.message });
    }
  };
}