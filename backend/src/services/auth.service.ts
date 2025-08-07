import jwt from 'jsonwebtoken';
import { UserModel } from '../models/user.model';
import prisma from '../config/database';

export class AuthService {
  private userModel: UserModel;
  
  constructor() {
    this.userModel = new UserModel();
  }

  /**
   * Register a new user
   */
  async register(userData: {
    email: string;
    password: string;
    firstName?: string;
    lastName?: string;
    companyName?: string;
    accountType?: string;
  }) {
    // Check if user already exists
    const existingUser = await this.userModel.findByEmail(userData.email);
    if (existingUser) {
      throw new Error('User with this email already exists');
    }

    // Create user transaction
    return prisma.$transaction(async (tx) => {
      // Create user
      const user = await tx.user.create({
        data: {
          email: userData.email,
          passwordHash: await this.userModel.hashPassword(userData.password),
        },
      });

      // Create profile if first name or last name provided
      if (userData.firstName || userData.lastName) {
        await tx.profile.create({
          data: {
            firstName: userData.firstName || '',
            lastName: userData.lastName || '',
            userId: user.id,
          },
        });
      }

      // Create business if company name provided
      if (userData.companyName) {
        await tx.business.create({
          data: {
            name: userData.companyName,
            userId: user.id,
          },
        });
      }

      // Create lender or borrower profile based on account type
      if (userData.accountType === 'lender' || userData.accountType === 'both') {
        await tx.lenderProfile.create({
          data: {
            userId: user.id,
          },
        });
      }

      if (userData.accountType === 'borrower' || userData.accountType === 'both') {
        await tx.borrowerProfile.create({
          data: {
            userId: user.id,
          },
        });
      }

      return user;
    });
  }

  /**
   * Login user
   */
  async login(email: string, password: string) {
    // Find user
    const user = await this.userModel.findByEmail(email);
    if (!user) {
      throw new Error('Invalid email or password');
    }

    // Verify password
    const isPasswordValid = await this.userModel.verifyPassword(password, user.passwordHash);
    if (!isPasswordValid) {
      throw new Error('Invalid email or password');
    }

    // Generate tokens
    const accessToken = this.generateAccessToken(user.id);
    const refreshToken = await this.generateRefreshToken(user.id);

    return {
      user,
      accessToken,
      refreshToken,
    };
  }

  /**
   * Refresh token
   */
  async refreshToken(token: string) {
    // Find refresh token
    const refreshTokenRecord = await prisma.refreshToken.findUnique({
      where: { token },
      include: { user: true },
    });

    // Validate token
    if (!refreshTokenRecord) {
      throw new Error('Invalid refresh token');
    }

    // Check if token is expired
    if (new Date() > refreshTokenRecord.expiresAt) {
      // Delete expired token
      await prisma.refreshToken.delete({
        where: { id: refreshTokenRecord.id },
      });
      throw new Error('Refresh token expired');
    }

    // Generate new tokens
    const accessToken = this.generateAccessToken(refreshTokenRecord.userId);
    const newRefreshToken = await this.generateRefreshToken(refreshTokenRecord.userId);

    // Delete old refresh token
    await prisma.refreshToken.delete({
      where: { id: refreshTokenRecord.id },
    });

    return {
      user: refreshTokenRecord.user,
      accessToken,
      refreshToken: newRefreshToken,
    };
  }

  /**
   * Logout user
   */
  async logout(token: string) {
    // Delete refresh token
    await prisma.refreshToken.deleteMany({
      where: { token },
    });
    return true;
  }

  /**
   * Generate access token
   */
  private generateAccessToken(userId: string) {
    const secret = process.env.JWT_SECRET || 'your-jwt-secret';
    const expiresIn = process.env.JWT_EXPIRES_IN || '1h';

    return jwt.sign({ userId }, secret, { expiresIn });
  }

  /**
   * Generate refresh token
   */
  private async generateRefreshToken(userId: string) {
    const secret = process.env.JWT_REFRESH_SECRET || 'your-jwt-refresh-secret';
    const expiresIn = process.env.JWT_REFRESH_EXPIRES_IN || '7d';

    // Generate token
    const token = jwt.sign({ userId }, secret, { expiresIn });

    // Calculate expiry date
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7); // 7 days

    // Save token to database
    await prisma.refreshToken.create({
      data: {
        token,
        userId,
        expiresAt,
      },
    });

    return token;
  }

  /**
   * Verify access token
   */
  verifyAccessToken(token: string) {
    try {
      const secret = process.env.JWT_SECRET || 'your-jwt-secret';
      const decoded = jwt.verify(token, secret) as { userId: string };
      return decoded;
    } catch (error) {
      throw new Error('Invalid token');
    }
  }
}