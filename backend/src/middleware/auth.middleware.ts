import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service';
import { UserModel } from '../models/user.model';

// Extend Express Request type to include user
declare global {
  namespace Express {
    interface Request {
      user?: any;
      userId?: string;
    }
  }
}

export class AuthMiddleware {
  private authService: AuthService;
  private userModel: UserModel;

  constructor() {
    this.authService = new AuthService();
    this.userModel = new UserModel();
  }

  /**
   * Authenticate user from JWT token
   */
  authenticate = async (req: Request, res: Response, next: NextFunction) => {
    try {
      // Get token from header
      const authHeader = req.headers.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ message: 'Authentication required' });
      }

      const token = authHeader.split(' ')[1];
      
      // Verify token
      const decoded = this.authService.verifyAccessToken(token);
      
      // Get user
      const user = await this.userModel.findById(decoded.userId);
      if (!user) {
        return res.status(401).json({ message: 'User not found' });
      }

      // Attach user to request
      req.user = user;
      req.userId = user.id;
      
      next();
    } catch (error) {
      return res.status(401).json({ message: 'Invalid token' });
    }
  };

  /**
   * Check if user has admin role
   */
  requireAdmin = (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ message: 'Authentication required' });
    }

    if (req.user.role !== 'ADMIN') {
      return res.status(403).json({ message: 'Admin access required' });
    }

    next();
  };

  /**
   * Check if user has lender profile
   */
  requireLender = async (req: Request, res: Response, next: NextFunction) => {
    if (!req.userId) {
      return res.status(401).json({ message: 'Authentication required' });
    }

    try {
      const userWithProfiles = await this.userModel.getFullProfile(req.userId);
      
      if (!userWithProfiles.lenderProfile) {
        return res.status(403).json({ message: 'Lender profile required' });
      }
      
      next();
    } catch (error) {
      return res.status(500).json({ message: 'Server error' });
    }
  };

  /**
   * Check if user has borrower profile
   */
  requireBorrower = async (req: Request, res: Response, next: NextFunction) => {
    if (!req.userId) {
      return res.status(401).json({ message: 'Authentication required' });
    }

    try {
      const userWithProfiles = await this.userModel.getFullProfile(req.userId);
      
      if (!userWithProfiles.borrowerProfile) {
        return res.status(403).json({ message: 'Borrower profile required' });
      }
      
      next();
    } catch (error) {
      return res.status(500).json({ message: 'Server error' });
    }
  };

  /**
   * Check if user has business profile
   */
  requireBusiness = async (req: Request, res: Response, next: NextFunction) => {
    if (!req.userId) {
      return res.status(401).json({ message: 'Authentication required' });
    }

    try {
      const userWithProfiles = await this.userModel.getFullProfile(req.userId);
      
      if (!userWithProfiles.business) {
        return res.status(403).json({ message: 'Business profile required' });
      }
      
      next();
    } catch (error) {
      return res.status(500).json({ message: 'Server error' });
    }
  };
}