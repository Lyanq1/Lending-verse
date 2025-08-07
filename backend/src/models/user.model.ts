import { User, UserRole } from '@prisma/client';
import prisma from '../config/database';
import bcrypt from 'bcrypt';

export class UserModel {
  /**
   * Find a user by email
   */
  async findByEmail(email: string): Promise<User | null> {
    return prisma.user.findUnique({
      where: { email },
    });
  }

  /**
   * Find a user by ID
   */
  async findById(id: string): Promise<User | null> {
    return prisma.user.findUnique({
      where: { id },
    });
  }

  /**
   * Create a new user
   */
  async create(data: {
    email: string;
    password: string;
    role?: UserRole;
  }): Promise<User> {
    const hashedPassword = await this.hashPassword(data.password);
    
    return prisma.user.create({
      data: {
        email: data.email,
        passwordHash: hashedPassword,
        role: data.role || 'USER',
      },
    });
  }

  /**
   * Update a user
   */
  async update(id: string, data: Partial<User>): Promise<User> {
    return prisma.user.update({
      where: { id },
      data,
    });
  }

  /**
   * Delete a user
   */
  async delete(id: string): Promise<User> {
    return prisma.user.delete({
      where: { id },
    });
  }

  /**
   * Verify password
   */
  async verifyPassword(plainPassword: string, hashedPassword: string): Promise<boolean> {
    return bcrypt.compare(plainPassword, hashedPassword);
  }

  /**
   * Hash password
   */
  async hashPassword(password: string): Promise<string> {
    const saltRounds = 10;
    return bcrypt.hash(password, saltRounds);
  }

  /**
   * Create or update profile
   */
  async createOrUpdateProfile(userId: string, profileData: any): Promise<any> {
    return prisma.profile.upsert({
      where: { userId },
      update: profileData,
      create: {
        ...profileData,
        userId,
      },
    });
  }

  /**
   * Create or update business
   */
  async createOrUpdateBusiness(userId: string, businessData: any): Promise<any> {
    return prisma.business.upsert({
      where: { userId },
      update: businessData,
      create: {
        ...businessData,
        userId,
      },
    });
  }

  /**
   * Create or update lender profile
   */
  async createOrUpdateLenderProfile(userId: string, lenderData: any): Promise<any> {
    return prisma.lenderProfile.upsert({
      where: { userId },
      update: lenderData,
      create: {
        ...lenderData,
        userId,
      },
    });
  }

  /**
   * Create or update borrower profile
   */
  async createOrUpdateBorrowerProfile(userId: string, borrowerData: any): Promise<any> {
    return prisma.borrowerProfile.upsert({
      where: { userId },
      update: borrowerData,
      create: {
        ...borrowerData,
        userId,
      },
    });
  }

  /**
   * Get user with full profile
   */
  async getFullProfile(userId: string): Promise<any> {
    return prisma.user.findUnique({
      where: { id: userId },
      include: {
        profile: true,
        business: true,
        lenderProfile: true,
        borrowerProfile: true,
      },
    });
  }
}